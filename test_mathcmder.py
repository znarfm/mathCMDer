import pytest
import sys
from mathcmder import generate, calculate, endgame, parse_args


def test_generate():
    assert generate("+", 1, 10) in [
        f"{x} + {y}" for x in range(1, 11) for y in range(1, 11)
    ]
    assert generate("-", 1, 10) in [
        f"{x} - {y}" for x in range(1, 11) for y in range(1, 11)
    ]
    assert generate("*", 1, 10) in [
        f"{x} * {y}" for x in range(1, 11) for y in range(1, 11)
    ]
    assert generate("/", 1, 10) in [
        f"{x*y} / {x}" for x in range(1, 11) for y in range(1, 11)
    ]


def test_calculate():
    assert calculate("5 + 3") == 8
    assert calculate("10 - 4") == 6
    assert calculate("2 * 7") == 14
    assert calculate("15 / 3") == 5


def test_endgame(mocker):
    mock_print = mocker.patch("builtins.print")
    mock_save_score = mocker.patch("mathcmder.save_score")

    # Use pytest.raises to handle the SystemExit exception
    with pytest.raises(SystemExit) as exc_info:
        endgame(False, "John Doe", 80, 5, 120.5, [12.05, 13.2, 14.1, 15.0, 16.15])

    # Check that SystemExit was raised with the correct message
    assert str(exc_info.value) == "This was CS50P!"

    # Check that print was called 4 times
    assert mock_print.call_count == 4

    # Check that save_score was called with correct arguments
    mock_save_score.assert_called_once_with(
        "John Doe", 80, 5, 120.5, 14.1, "leaderboard.db"
    )


def test_parse_args():
    # Test start command with required arguments
    sys.argv[1:] = ["start", "-c", "10", "-o", "+"]
    args = parse_args()
    assert args.command == "start"
    assert args.count == 10
    assert args.operation == "+"

    # Test leaderboard command with optional arguments
    sys.argv[1:] = ["leaderboard", "-s", "score", "-o", "*"]
    args = parse_args()
    assert args.command == "leaderboard"
    assert args.leaderboard_sort == "score"
    assert args.leaderboard_operation == "*"


if __name__ == "__main__":
    pytest.main()
