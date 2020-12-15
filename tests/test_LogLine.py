from Types import LogLine


def test_LogLine_ConvertStringToTime_should_convert_trueDate_to_timeStamp():
    # Arrange
    date_as_string = '2020-09-29T08:42:42.034629+02:00'
    expected_result = "1601361762.034629"

    # Act
    date_as_epoch = LogLine.ConvertStringToTime(date_as_string)

    # Assert
    assert str(date_as_epoch) == expected_result


def test_LogLine_ConvertTimestampToString_should_convert_timestamp_to_trueDate():
    # Arrange
    date_as_epoch = 1601361762.034629
    expected_result = '2020-09-29-08:42:42.034629'

    # Act
    date_as_string = LogLine.ConvertTimestampToString(date_as_epoch)

    # Assert
    assert date_as_string == expected_result


def test_LogLine_Should_parse_input():
    # arrange
    logline_as_string = '2020-12-11T10:21:46.6697472+01:00 [INF] "GalaxySiteSelector" - service version: "0.9.5.5", library version: "0.9.5.9" - machinename: "AX86506" (SiteSelector.Program) (b27fd4b2)'
    expected_time = 1607678506.669747
    expected_payload = '[INF] "GalaxySiteSelector" - service version: "0.9.5.5", library version: "0.9.5.9" - machinename: "AX86506" (SiteSelector.Program) (b27fd4b2)'

    # act
    logline = LogLine(logline_as_string)
    time = logline.GetTimeStamp() 
    payload = logline.GetPayLoad()

    # asssert
    assert time is not None
    assert time == expected_time
    assert payload is not None
    assert payload == expected_payload
