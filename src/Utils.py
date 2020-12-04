import Types
from Types import Terminator as Terminator


class Utils:

    @staticmethod
    def Pointer_ToString(pointer):
        h = '$$'  # header
        s = '$'  # separator

        to_string = f'{h}{pointer.client}{s}{pointer.date}{s}{pointer.linenumber}{s}{pointer.payload}'
        return to_string

    @staticmethod
    def Pointer_ToTerminator(string):
        h = '$$'  # header
        s = '$'  # separator

        payload_parts = string.split(h)[1].split(s)   
        if payload_parts[3] == 'None': payload_parts[3] = None  # Survive the stringiness
        terminator = Terminator(payload_parts[0], payload_parts[1], int(payload_parts[2]), payload_parts[3])
        return terminator





if __name__ == "__main__":
    term = Terminator("Client", "19700101", "888", None)
    as_string = Utils.Pointer_ToString(term)
    as_term = Utils.Pointer_ToTerminator(as_string)
    print(as_string, as_term)
