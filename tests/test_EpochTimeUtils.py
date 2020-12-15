from Utils import EpochTimeUtil as EpochTimeUtil


def test_DeltaTimeWrap_should_produce_expected_result():
    # arrange
    t_delta_epoch = 0.1853020191
    expected_result = '00000000001853020191'

    # act
    wrapped = EpochTimeUtil.DeltaTimeWrap(t_delta_epoch)

    # assert
    assert wrapped == expected_result


def test_DeltaTimeUnWrap_should_produce_expected_result():
    # arrange
    wrapped_delta = '00000000001853020191'
    expected_result = 0.1853020191

    # act
    unwrapped = EpochTimeUtil.DeltaTimeUnWrap(wrapped_delta)

    # assert
    assert unwrapped == expected_result
