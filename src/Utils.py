from Types import Terminator as Terminator


class TermUtil:
    """
    Utililites for transforming Termintor tuples to and from strings.
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

    def ListToLinked(term_list):
        """
        Take a list of terminators, and build a linked-list.
        """
        def inner(term_list):
            if len(term_list) < 2:
                return Terminator(term_list[0].client, term_list[0].date, term_list[0].linenumber, None)
            return Terminator(term_list[0].client, term_list[0].date, term_list[0].linenumber, TermUtil.ToString(inner(term_list[1:])))
        return TermUtil.ToString(inner(term_list))

    def LinkedToList(pointers_string):
        """
        Transform string-object to list of Terminator
        """
        if not str(pointers_string):
            raise Exception("Argument must be a string")
        
        h = TermUtil.h
        pointers_list = []
        
        parts = pointers_string.split(h)[1:]
        for part in parts:
            terminator = TermUtil.ToTerminator(f'@{part}')  # we must re-add header to stripped part
            pointers_list.append(terminator)
        return pointers_list

if __name__ == "__main__":
    term = Terminator("Client", "19700101", "888", None)
    as_string = TermUtil.ToString(term)
    as_term = TermUtil.ToTerminator(as_string)
    print(as_string, as_term)

    terminators = []
    terminators.append(Terminator("client1", "date1", 1, None))
    terminators.append(Terminator("client2", "date2", 2, None))
    terminators.append(Terminator("client3", "date3", 3, None))
    linked = TermUtil.ListToLinked(terminators)
    _list = TermUtil.LinkedToList(linked)
    print(_list)
