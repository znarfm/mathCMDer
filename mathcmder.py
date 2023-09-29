import argparse
import time
from random import randint
from pytimedinput import timedInput


def main():
    """
    Executes the main logic of the program.

    This function parses the command line arguments, starts the quiz,
    and ends the quiz.

    Parameters:
        None

    Returns:
        None
    """
    # Parse arguments
    args = parse_args()

    # Start the quiz
    score, total_time, time_list = run_quiz(args)

    # End the quiz
    endgame(score, total_time, args.count, time_list)


def parse_args():
    """
    Parse the command line arguments to configure the math quiz.

    Parameters:
        None

    Returns:
        argparse.Namespace: An object containing the parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="A simple math quiz CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        epilog="This is a project by Meinard for CS50P",
    )
    parser.add_argument(
        "-c",
        "--count",
        metavar="NUMBER_OF_QUESTIONS",
        help="enter number of questions you want to answer",
        type=int,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--operation",
        help="enter which operation you want to quiz",
        type=str,
        choices=["+", "-", "*"],
        required=True,
    )
    parser.add_argument(
        "-l", "--lowest", help="enter the lowest operand value", type=int, default=1
    )
    parser.add_argument(
        "-m",
        "--max",
        help="enter the highest operand value",
        dest="highest",
        type=int,
        default=10,
    )
    parser.add_argument(
        "-t",
        "--timer",
        metavar="SECONDS",
        help="set a timeout for each question",
        type=int,
        default=-1,
    )

    args = parser.parse_args()

    if args.lowest > args.highest:
        parser.error(
            "lowest operand cannot be greater than highest operand"
        )

    return args


def generate(operation: str, lowest: int, highest: int) -> str:
    """
    Generate a random arithmetic expression.

    Parameters:
        operation (str): The arithmetic operation to be performed.
        lowest (int): The lowest possible value for the operands.
        highest (int): The highest possible value for the operands.

    Returns:
        str: The arithmetic expression as a string.

    """
    num1 = randint(lowest, highest)
    num2 = randint(lowest, highest)

    return f"{num1} {operation} {num2}"


def calculate(question: str) -> int:
    """
    Calculate the result of a mathematical operation.

    Args:
        question (str): A string representing a mathematical operation. The
            format of the string should be "<num1> <operation> <num2>", where
            <num1> and <num2> are integers and <operation> is one of "+", "-",
            or "*".

    Returns:
        int: The result of the mathematical operation.

    Raises:
        ValueError: If the question string is not in the correct format or if
            the operation is not supported.

    Example:
        >>> calculate("5 + 3")
        8
        >>> calculate("10 * 2")
        20
    """
    try:
        num1, operation, num2 = question.split()
        num1 = int(num1)
        num2 = int(num2)
    except ValueError:
        raise ValueError("Invalid question format")

    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    else:
        raise ValueError("Unsupported operation")


def run_quiz(args: object) -> tuple:
    """
    Run a quiz with the given arguments.

    Args:
        args (object): An object containing the arguments for running the quiz.

    Returns:
        tuple: A tuple containing the score (int), total time (float), and a list of question times (list[float]).
    """
    score = 0
    time_list = []
    start_time = time.time()

    for i in range(args.count):
        question = generate(args.operation, args.lowest, args.highest)
        correct = calculate(question)
        question_time_start = time.time()

        ans, timed_out = timedInput(
            f"Q#{i+1}\t{question} = ", timeout=args.timer, resetOnInput=False
        )

        # Catch error in case user inputs something other than a number
        try:
            if timed_out:
                print("Timed out! ❌")
            elif correct == int(ans):
                score += 1
                print("Correct! ✅")
            else:
                print("Incorrect. ❌")
        except ValueError:
            pass

        question_time_end = time.time()
        time_list.append(question_time_end - question_time_start)

    end_time = time.time()
    total_time = end_time - start_time

    return score, total_time, time_list


def endgame(score: int, total_time: float, count: int, time_list: list) -> None:
    """
    Print the endgame summary including the player's score, the total time taken, the number of questions answered, and the average time per question.

    Parameters:
    - score (int): The player's score in the quiz.
    - total_time (float): The total time taken by the player to complete the quiz.
    - count (int): The number of questions answered by the player.
    - time_list (list): A list of the time taken for each question.

    Returns:
    - None: This function does not return any value.
    """
    print("\nQuiz finished!")
    print(f"Your score is {score} out of {count}")
    print(f"You finished in {total_time:.02f}s")
    print(f"Average time per question: {sum(time_list) / count:.02f}s")
    raise SystemExit("This is CS50P!")


if __name__ == "__main__":
    main()
