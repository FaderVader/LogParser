from ..LogLine import LogLine

def test_LogLine_Should_Convert_TrueDate_To_TimeStamp():
    # Arrange
    date_as_string = '2020-09-29T08:42:42.034629+02:00'
    expected_result = "1601361762.034629"

    # Act
    date_as_epoch = LogLine.parseStringToTime(date_as_string)

    # Assert
    assert str(date_as_epoch) == expected_result


def test_LogLine_Should_Convert_Timestamp_To_TrueDate():
    # Arrange
    date_as_epoch = 1601361762.034629
    expected_result = '2020-09-29-08:42:42.034629'

    # Act
    date_as_string = LogLine.parseTimeStampToString(date_as_epoch)

    # Assert
    assert date_as_string == expected_result

