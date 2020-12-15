from Types import Terminator as Terminator


class TermUtil:
    """
    Utililites for transforming Terminator tuples to and from strings.
    """
    h = '@'  # header
    s = '$'  # separator

    @staticmethod
    def ToString(pointer):
        """
        Takes an Terminator (pointer) and returns a specially formatted string.
        Usefull for building linked.list terminators.
        """
        h = TermUtil.h
        s = TermUtil.s
        to_string = f'{h}{pointer.client}{s}{pointer.date}{s}{pointer.linenumber}{s}{pointer.payload}'
        return to_string

    @staticmethod
    def ToTerminator(string):
        """
        Takes a specially formatted string, and returns a Terminator.
        Usefull for building linked.list terminators.
        """
        h = TermUtil.h
        s = TermUtil.s
        try:
            payload_parts = string.split(h)[1].split(s)   
            if payload_parts[3] == 'None' or payload_parts[3] == '': 
                payload_parts[3] = None  # Survive the stringiness
            terminator = Terminator(payload_parts[0], payload_parts[1], int(payload_parts[2]), payload_parts[3])
            return terminator
        except AttributeError:
            return None  # if we cannot parse string, we return empty - do not throw - any other exception throws
        except:
            raise Exception("Error in TermUtil.ToTerminator")

    @staticmethod
    def ListToLinkedString(term_list):
        """
        Recursively transforms a list of terminators.\n
        Returns first Terminator, with remaining terminators converted to embedded payload.
        """
        def inner(term_list):
            if len(term_list) < 2:
                return Terminator(term_list[0].client, term_list[0].date, term_list[0].linenumber, None)
            return Terminator(term_list[0].client, term_list[0].date, term_list[0].linenumber, TermUtil.ToString(inner(term_list[1:])))
        return inner(term_list)  # return TermUtil.ToString(inner(term_list)) (completely stringified result)

    @staticmethod  # 
    def StringToListOfPointers(pointers_string):
        """
        Transform string-object to list of Terminators, with no payload.
        """
        if not str(pointers_string):
            raise Exception("Argument must be a string")

        h = TermUtil.h
        pointers_list = []

        parts = pointers_string.split(h)[1:]
        pointers_list = [TermUtil.ToTerminator(f'@{part}') for part in parts]
        return pointers_list

    @staticmethod
    def StringToPointerWithPayload(string):
        """
        Converts '@client1$date1$1$@client2$date2$2$@client3$date3$3$None' -> \n
        Terminator(client='client1', date='date1', linenumber=1, payload='@client2$date2$2$@client3$date3$3$None')
        """
        converted = TermUtil.StringToListOfPointers(string)
        pointer = TermUtil.ListToLinkedString(converted)
        return pointer


class EpochTimeUtil:
    """
    Utilities for wrapping/unwrapping time intervals expressed in epoch-format.
    """
    delta_factor = 10**10  # multiply time-data by factor      
    delta_padding = 20     # defines format of time-data for uniform sorting-behavior

    @staticmethod
    def DeltaTimeWrap(t_delta_epoch):
        """
        Convert 0.1853020191 -> 00000000001853020191
        """
        t_delta_factored = t_delta_epoch * EpochTimeUtil.delta_factor
        t_delta_string = (f'{t_delta_factored}').split('.')[0]  # ditch the dot
        length = len(t_delta_string)
        t_delta_formatted = ('0' * (EpochTimeUtil.delta_padding - length)) + t_delta_string  # pad with leading zero's
        return t_delta_formatted

    @staticmethod
    def DeltaTimeUnWrap(t_delta_string):
        """
        Convert 00000000001853020191 -> 0.1853020191
        """
        t_delta_int = int(t_delta_string) / EpochTimeUtil.delta_factor
        return t_delta_int


if __name__ == "__main__":
    term = Terminator("Client", "19700101", "888", None)
    as_string = TermUtil.ToString(term)
    as_term = TermUtil.ToTerminator(as_string)
    print(as_string, as_term)

    terminators = []
    terminators.append(Terminator("client1", "date1", 1, None))
    terminators.append(Terminator("client2", "date2", 2, None))
    terminators.append(Terminator("client3", "date3", 3, None))
    linked = TermUtil.ListToLinkedString(terminators)
    print(linked)

    payload = '@client1$date1$1$@client2$date2$2$@client3$date3$3$None'
    converted = TermUtil.StringToListOfPointers(payload)
    pointer = TermUtil.ListToLinkedString(converted)
    print(pointer)

    time_epoch = 0.1408741474
    wrapped = EpochTimeUtil.DeltaTimeWrap(time_epoch)
    unwrapped = EpochTimeUtil.DeltaTimeUnWrap(wrapped)
    print(time_epoch, wrapped, unwrapped)
