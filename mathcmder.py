import argparse
import sqlite3
import time
from random import randint
from pytimedinput import timedInput
from tabulate import tabulate


def main():
    # SQLite
    conn = sqlite3.connect("leaderboard.db")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS leaderboard (date text, name text, score integer, count integer, time real, avg real)"
    )
    conn.commit()
    conn.close()

    # Parse arguments
    args = parse_args()

    if args.command == "start":
        if args.name is None and not args.opt_out:
            args.name = input("Enter your name: ")
        # Start the quiz
        score, total_time, time_list = run_quiz(args)
        # End the quiz
        endgame(args.opt_out, args.name, score, args.count, total_time, time_list)
    elif args.command == "leaderboard":
        # Show the leaderboard
        read_leaderboard(args)


def parse_args():
    """
    Parse the command line arguments to configure the math quiz.

    Returns:
        argparse.Namespace: An object containing the parsed command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="A simple math quiz CLI",
        epilog="This is a project by Meinard for CS50P",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND", required=True)

    # Sub parser: start
    start_parser = subparsers.add_parser(
        "start",
        help="start the quiz",
    )
    name_group = start_parser.add_mutually_exclusive_group()
    name_group.add_argument(
        "-n",
        "--name",
        metavar="NAME",
        help="enter your name",
        type=str,
    )
    name_group.add_argument(
        "-nl",
        "--no-leaderboard",
        dest="opt_out",
        help="opt out of the leaderboard (default: False)",
        action="store_true",
    )
    start_parser.add_argument(
        "-c",
        "--count",
        metavar="NUMBER_OF_QUESTIONS",
        help="enter number of questions you want to answer",
        type=int,
        required=True,
    )
    start_parser.add_argument(
        "-o",
        "--operation",
        help="enter which operation you want to quiz",
        type=str,
        choices=["+", "-", "*", "/"],
        required=True,
    )
    start_parser.add_argument(
        "-l",
        "--lowest",
        help="enter the lowest operand value (note: for division problems, this will be the lowest possible divisor; default: 1)",
        metavar="LOWEST_OPERAND",
        type=int,
        default=1,
    )
    start_parser.add_argument(
        "-m",
        "--max",
        help="enter the highest operand value (note: for division problems, this will be the highest possible divisor; default: 10)",
        dest="highest",
        metavar="HIGHEST_OPERAND",
        type=int,
        default=10,
    )
    start_parser.add_argument(
        "-t",
        "--timer",
        metavar="SECONDS",
        help="set a timeout for each question (default: no timeout)",
        type=int,
        default=-1,
    )

    # Sub parser: show scores
    lb_parser = subparsers.add_parser(
        "leaderboard",
        help="prints out the leaderboard",
    )

    lb_parser.add_argument(
        "-s",
        "--sort",
        dest="leaderboard_sort",
        help="sort the leaderboard (best to worst) according to a column",
        choices=["score", "time", "count", "avg"],
    )

    lb_parser.add_argument(
        "-o",
        "--operation",
        dest="leaderboard_operation",
        help="enter which operation to show leaderboard for",
        type=str,
        choices=["+", "-", "*", "/"],
    )

    lb_parser.add_argument(
        "-n",
        "--name",
        metavar="NAME",
        dest="leaderboard_name",
        help="enter which name to show leaderboard for",
        type=str,
    )

    args = parser.parse_args()

    if args.command == "start" and args.lowest > args.highest:
        parser.error("lowest operand cannot be greater than highest operand")

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
    # To avoid division by zero
    if lowest == 0:
        lowest = randint(1, highest)

    num1 = randint(lowest, highest)
    num2 = randint(lowest, highest)

    return (
        f"{num1 * num2} {operation} {num1}"
        if operation == "/"
        else f"{num1} {operation} {num2}"
    )


def calculate(question: str) -> int:
    """Calculate the result of an arithmetic expression.

    Args:
        question (str): A string representing an arithmetic expression. The format of the string should be "<num1> <operation> <num2>", where <num1> and <num2> are integers and <operation> is one of "+", "-", "*", or "/".

    Raises:
        ValueError: If the question string is not in the correct format.

    Returns:
        int: The result of the arithmetic expression.
    """
    try:
        num1, operation, num2 = question.split()
        num1 = int(num1)
        num2 = int(num2)
    except ValueError:
        raise ValueError("Invalid question format")

    match operation:
        case "+":
            return num1 + num2
        case "-":
            return num1 - num2
        case "*":
            return num1 * num2
        case "/":
            return num1 // num2


def run_quiz(args: object) -> tuple:
    """
    Run a quiz with the given arguments.

    Args:
        args (object): An object returned by parse_args().

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

        user_input = None
        try:
            if args.timer >= 0:
                user_input, timed_out = timedInput(
                    f"Q#{i+1}\t{question} = ", timeout=args.timer, resetOnInput=False
                )
                if timed_out:
                    print("Timed out! ❌⌛")
                    user_input = None
            else:
                user_input = input(f"Q#{i+1}\t{question} = ")
        except KeyboardInterrupt:
            print("Quitting quiz...")
            raise SystemExit
        except TypeError:
            pass

        try:
            if not user_input.isnumeric() or int(user_input) != correct:
                print("Incorrect. ❌")
            else:
                score += 1
                print("Correct! ✅")
        except (ValueError, TypeError, AttributeError):
            pass

        question_time_end = time.time()
        time_list.append(question_time_end - question_time_start)

    end_time = time.time()
    total_time = end_time - start_time

    return score, total_time, time_list


def save_score(
    name: str, score: int, count: int, total_time: float, ave: float, db_name: str = "leaderboard.db"
) -> None:
    """
    Save the score of a player in the leaderboard.

    Args:
        name (str): The name of the player.
        score (int): The score achieved by the player.
        total_time (float): The total time taken by the player.
        count (int): The number of questions attempted by the player.
        ave (float): The average time taken per question by the player.
        db_name (str, optional): The name of the SQLite database file. Defaults to "leaderboard.db".

    Returns:
        None: This function does not return anything.
    """

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        "INSERT INTO leaderboard VALUES (CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)",
        (name, score, count, total_time, ave),
    )
    conn.commit()
    conn.close()


def endgame(
    opt_out: bool, name: str, score: int, count: int, total_time: float, time_list: list
) -> None:
    """
    Prints the endgame message with the player's score, total time, and average time per question, and saves the score to a file.

    Parameters:
        opt_out (bool): Whether the user opted out of the leaderboard.
        name (str): The name of the player.
        score (int): The player's score.
        count (int): The total number of questions in the quiz.
        total_time (float): The total time taken to complete the quiz in seconds.
        time_list (list): A list of the time taken for each question.

    Returns:
        None
    """

    ave = sum(time_list) / count
    print("\nQuiz finished!")
    print(f"Your score is {score} out of {count}")
    print(f"You finished in {total_time:.02f}s")
    print(f"Average time per question: {ave:.02f}s")
    if not opt_out:
        save_score(name, score, count, total_time, ave, "leaderboard.db")
    raise SystemExit("This was CS50P!")


def read_leaderboard(args: object, db_name: str = "leaderboard.db") -> None:
    """
    Reads the leaderboard data from the SQLite database "leaderboard.db" and displays it in a fancy grid format.
    If the database is empty, it prints a message indicating that the leaderboard is empty.

    Parameters:
        args (object): An object returned by parse_args().

    Returns:
        None
    """

    query = "SELECT * FROM leaderboard WHERE 1=1"
    params = []
    if args.leaderboard_operation is not None:
        query += " AND operation = ?"
        params.append(args.leaderboard_operation)
    if args.leaderboard_name is not None:
        query += " AND name = ?"
        params.append(args.leaderboard_name)

    if args.leaderboard_sort in ["score", "count"]:
        query += f" ORDER BY {args.leaderboard_sort} DESC"
    elif args.leaderboard_sort in ["time", "avg"]:
        query += f" ORDER BY {args.leaderboard_sort} ASC"

    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()

    if rows:
        print(
            tabulate(
                rows,
                headers=[
                    "Date",
                    "Name",
                    "Score",
                    "Question Count",
                    "Time",
                    "Avg. Time/Question",
                ],
                tablefmt="fancy_grid",
            )
        )
    elif args.leaderboard_name is not None:
        print(f"No results found for name {args.leaderboard_name}.")
    else:
        print("Leaderboard is empty.")


if __name__ == "__main__":
    main()
