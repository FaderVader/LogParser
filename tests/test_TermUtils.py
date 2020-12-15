from Types import Terminator as Terminator
from Utils import TermUtil as TermUtil


def test_ToTerminator_should_produce_expected_output():
    # arrange
    pointer_as_string = "@XX$YY$1$None"
    expected_result = Terminator(client="XX", date="YY", linenumber=1, payload=None)

    # act
    term_as_type = TermUtil.ToTerminator(pointer_as_string)

    # assert
    assert term_as_type == expected_result


def test_ToString_should_produce_expected_output():
    # arrange
    pointer_as_string = Terminator(client="XX", date="YY", linenumber=1, payload=None)
    expected_result = "@XX$YY$1$None"

    # act
    term_as_string = TermUtil.ToString(pointer_as_string)    

    # assert
    assert term_as_string == expected_result


def test_StringToPointerWithPayload_should_produce_expected_output():
    # arrange
    pointer_with_payload = '@client1$date1$1$@client2$date2$2$@client3$date3$3$None'
    expected_result = Terminator(client='client1', date='date1', linenumber=1, payload='@client2$date2$2$@client3$date3$3$None')

    # act
    terminator = TermUtil.StringToPointerWithPayload(pointer_with_payload)

    # assert
    assert terminator == expected_result


def test_ListToLinkedString_should_produce_expected_output():
    # arrange
    pointers = [Terminator(client="AA", date="AA", linenumber=1, payload=None),
    Terminator(client="BB", date="BB", linenumber=2, payload=None),
    Terminator(client="CC", date="CC", linenumber=3, payload=None)]
    expected_result = Terminator(client="AA", date="AA", linenumber=1, payload="@BB$BB$2$@CC$CC$3$None")

    # act
    term_with_payload = TermUtil.ListToLinkedString(pointers)    

    # assert
    assert term_with_payload == expected_result


def test_StringToListOfPointers_should_produce_expected_output():
    # arrange
    pointer_with_payload = '@AA$AA$1$@BB$BB$2$@CC$CC$3$None'
    expected_result = [Terminator(client="AA", date="AA", linenumber=1, payload=None),
    Terminator(client="BB", date="BB", linenumber=2, payload=None),
    Terminator(client="CC", date="CC", linenumber=3, payload=None)]

    # act
    term_with_payload = TermUtil.StringToListOfPointers(pointer_with_payload)    

    # assert
    assert term_with_payload == expected_result
