import sys
import pytest
from mathcmder import *


@pytest.mark.parametrize(
    "test_args, expected",
    [
        (
            ["-c", "10", "-o", "+", "-l", "1", "-m", "10", "-t", "30"],
            {"count": 10, "operation": "+", "lowest": 1, "highest": 10, "timer": 30},
        ),
        (
            ["-c5", "-o-", "-l2", "-m8", "-t15"],
            {"count": 5, "operation": "-", "lowest": 2, "highest": 8, "timer": 15},
        ),
        (
            [
                "--count",
                "10",
                "--operation",
                "+",
                "--lowest",
                "1",
                "--max",
                "10",
                "--timer",
                "30",
            ],
            {"count": 10, "operation": "+", "lowest": 1, "highest": 10, "timer": 30},
        ),
    ],
)
def test_parse_args(test_args, expected):
    sys.argv[1:] = test_args
    args = parse_args()
    assert args.count == expected["count"]
    assert args.operation == expected["operation"]
    assert args.lowest == expected["lowest"]
    assert args.highest == expected["highest"]
    assert args.timer == expected["timer"]


def test_parse_args_no_args():
    sys.argv[1:] = []
    with pytest.raises(SystemExit):
        parse_args()


def test_generate():
    # Addition
    result = generate("+", 1, 10)
    num1, operation, num2 = result.split()
    num1 = int(num1)
    num2 = int(num2)
    assert 1 <= num1 <= 10
    assert 1 <= num2 <= 10
    assert operation == "+"

    # Subtraction
    result = generate("-", 1, 10)
    num1, operation, num2 = result.split()
    num1 = int(num1)
    num2 = int(num2)
    assert 1 <= num1 <= 10
    assert 1 <= num2 <= 10
    assert operation == "-"

    # Multiplication
    result = generate("*", 1, 10)
    num1, operation, num2 = result.split()
    num1 = int(num1)
    num2 = int(num2)
    assert 1 <= num1 <= 10
    assert 1 <= num2 <= 10
    assert operation == "*"

    # Negative numbers
    result = generate("+", -10, -1)
    num1, operation, num2 = result.split()
    num1 = int(num1)
    num2 = int(num2)
    assert -10 <= num1 <= -1
    assert -10 <= num2 <= -1
    assert operation == "+"


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("5 + 3", 8),
        ("10 - 2", 8),
        ("5 * 3", 15),
    ],
)
def test_calculate(test_input, expected):
    result = calculate(test_input)
    assert result == expected

    # Invalid format
    with pytest.raises(ValueError):
        calculate("5 +")

    # Unsupported operation
    with pytest.raises(ValueError):
        calculate("5 / 2")


def test_run_quiz():
    class MockArgs:
        def __init__(self, count, operation, lowest, highest, timer):
            self.count = count
            self.operation = operation
            self.lowest = lowest
            self.highest = highest
            self.timer = timer

    args = MockArgs(count=3, operation="+", lowest=0, highest=10, timer=5)
    score, total_time, time_list = run_quiz(args)

    assert isinstance(score, int)
    assert isinstance(total_time, float)
    assert isinstance(time_list, list)
    assert len(time_list) == 3


def test_endgame():
    score = 8
    total_time = 30.5
    count = 10
    time_list = [3.2, 2.5, 4.1, 2.9, 3.7, 3.8, 4.5, 3.1, 2.6, 2.9]

    # Call the function and capture the printed output
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        endgame(score, total_time, count, time_list)

    # Assert the expected output
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == "This is CS50P!"
