from Types import Terminator as Terminator


class TermUtil:
    """
    Utililites for transforming Termintor tuples to and from strings.
    """
    h = '$$'  # header
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
            if payload_parts[3] == 'None': payload_parts[3] = None  # Survive the stringiness
            terminator = Terminator(payload_parts[0], payload_parts[1], int(payload_parts[2]), payload_parts[3])
            return terminator
        except AttributeError:
            return None  # if we cannot parse string, we return empty - do not throw - any other exception throws


if __name__ == "__main__":
    term = Terminator("Client", "19700101", "888", None)
    as_string = TermUtil.ToString(term)
    as_term = TermUtil.ToTerminator(as_string)
    print(as_string, as_term)
