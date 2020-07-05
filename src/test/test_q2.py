import pytest
import logging
from src import q2

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class InputOutputCase():
    """Represents a test case with input_val and expected expected_output"""

    def __init__(self, name, input_val, expected_output):
        self.name = name
        self.input_val = input_val
        self.expected_output = expected_output


test_downsample_time = [
    InputOutputCase(
        name="Nominal",
        input_val=[1, 1, 1, 1, 10],
        expected_output=[1, 5]
    )
]


@ pytest.mark.parametrize("case", test_downsample_time)
def test_downsample_time(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    result = downsample_time(case.input_val, 2)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)


test_downsample_amplitude = [
    InputOutputCase(
        name="Nominal",
        input_val=[234, 231, 178, 156, 104],
        expected_output=[3, 3, 2, 2, 1]
    )
]


@ pytest.mark.parametrize("case", test_downsample_amplitude)
def test_downsample_amplitude(case):
    log.info("Case: " + case.name)
    log.debug("Input: " + str(case.input_val))

    result = downsample_amplitude(case.input_val, 256, 4)

    log.debug("Result: " + str(result))
    assert(result == case.expected_output)
