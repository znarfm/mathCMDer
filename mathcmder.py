import argparse
import sqlite3
import time
from random import randint
from pytimedinput import timedInput
from tabulate import tabulate


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

    # SQLite
    conn = sqlite3.connect("leaderboard.db")
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS leaderboard (name text, score integer, time real, count integer, avg real)"
    )
    conn.commit()
    conn.close()

    # Parse arguments
    args = parse_args()

    if args.command == "start":
        # Start the quiz
        score, total_time, time_list = run_quiz(args)
        # End the quiz
        endgame(args.name, score, total_time, args.count, time_list)
    elif args.command == "leaderboard":
        # Show the leaderboard
        read_leaderboard()


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
    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # Sub parser: start
    start_parser = subparsers.add_parser(
        "start",
        help="start the quiz",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    start_parser.add_argument(
        "-n",
        "--name",
        metavar="NAME",
        help="enter your name",
        type=str,
        default="Anonymous",
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
        help="enter the lowest operand value (note: for division problems, this will be the lowest possible divisor)", 
        type=int, 
        default=1
    )
    start_parser.add_argument(
        "-m",
        "--max",
        help="enter the highest operand value (note: for division problems, this will be the highest possible divisor)",
        dest="highest",
        type=int,
        default=10,
    )
    start_parser.add_argument(
        "-t",
        "--timer",
        metavar="SECONDS",
        help="set a timeout for each question",
        type=int,
        default=-1,
    )

    # Sub parser: show scores
    subparsers.add_parser(
        "leaderboard",
        help="prints out the leaderboard",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    
    args = parser.parse_args()

    if args.command == "start" and args.lowest > args.highest:
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
    # To avoid division by zero
    if lowest == 0:
        lowest = randint(1, highest)
    
    num1 = randint(lowest, highest)
    num2 = randint(lowest, highest)
    
    if operation == "/":
        return f"{num1 * num2} {operation} {num1}"
    else:
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
    elif operation == "/":
        return num1 // num2
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

def save_score(name: str, score: int, total_time: float, count: int, ave: float) -> None:
    """
    Save the score of a player in the leaderboard.

    Args:
        name (str): The name of the player.
        score (int): The score achieved by the player.
        total_time (float): The total time taken by the player.
        count (int): The number of questions attempted by the player.
        ave (float): The average time taken per question by the player.

    Returns:
        None: This function does not return anything.
    """

    conn = sqlite3.connect("leaderboard.db")
    c = conn.cursor()
    c.execute("INSERT INTO leaderboard VALUES (?, ?, ?, ?, ?)", (name, score, total_time, count, ave))
    conn.commit()
    conn.close()

def endgame(name: str, score: int, total_time: float, count: int, time_list: list) -> None:
    """
    Prints the endgame message with the player's score, total time, and average time per question, and saves the score to a file.

    Parameters:
        name (str): The name of the player.
        score (int): The player's score.
        total_time (float): The total time taken to complete the quiz in seconds.
        count (int): The total number of questions in the quiz.
        time_list (list): A list of the time taken for each question.

    Returns:
        None
    """
    
    print("\nQuiz finished!")
    print(f"Your score is {score} out of {count}")
    print(f"You finished in {total_time:.02f}s")
    ave = sum(time_list) / count
    print(f"Average time per question: {ave:.02f}s")
    save_score(name, score, total_time, count, ave)
    raise SystemExit("This was CS50P!")

def read_leaderboard():
    """
    Reads the leaderboard data from the SQLite database "leaderboard.db" and displays it in a fancy grid format.
    If the database is empty, it prints a message indicating that the leaderboard is empty.

    Parameters:
        None

    Returns:
        None
    """

    conn = sqlite3.connect("leaderboard.db")
    c = conn.cursor()
    c.execute("SELECT * FROM leaderboard")
    rows = c.fetchall()
    conn.close()

    if rows:
        print(tabulate(rows, headers=["Name", "Score", "Time", "Question Count", "Avg. Time/Question"], tablefmt='fancy_grid'))
    else:
        print("Leaderboard is empty.")

if __name__ == "__main__":
    main()
