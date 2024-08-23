# MathCMDer

## Description

MathCMDer is a command-line interface (CLI) math quiz application written in Python. It allows users to test their math skills by answering a series of arithmetic questions.

This is a project for [CS50P](https://cs50.harvard.edu/python/).

## Features

- Customizable number of questions
- Choose from addition, subtraction, multiplication, or division operations
- Set a range of operand values
- *Optional* timer for each question
- Local leaderboard (using SQLite)

## Installation

Make sure you have Python installed to run this program.

1. Clone the repository

    ```bash
    git clone https://github.com/znarfm/mathCMDer.git && cd mathCMDer
    ```

2. Create a virtual environment and activate it

    On Windows:

    ```bash
    python -m venv venv
    ./venv/Scripts/activate
    ```

    On macOS and Linux:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

MathCMDer allows you to start a quiz or view the leaderboard.

### Start a quiz

```bash
python mathcmder.py start [options]
```

Available options:

- **`-c` or `--count`**: Set the number of questions
- **`-o` or `--operation`**: Set the math operation (+, -, *, /)
- `-l` or `--lowest`: Set the lowest operand value (default: 1)
- `-m` or `--max`: Set the highest operand value (default: 10)
- `-t` or `--timer`: Set a timeout (in seconds) for each question (default: no timeout)
- `-n` or `--name`: Set the name to be saved in the leaderboard (Default: Anonymous)
- `-nl` or `--no-leaderboard`: Opt out of the leaderboard

Example usage:

```bash
python mathcmder.py start -c 10 -o+ -l 1 -m 10 -t 5 -n "Juan"
```

This will start the program with 10 addition questions, using operands from 1 to 10, and a timeout of 5 seconds for each question. The name `Juan` instead of `Anonymous` will appear in the leaderboard.

```bash
python mathcmder.py start -c15 -o* -nl
```

This will start the program with 15 multiplication questions, using the default operand values (1 to 10) without a timeout, and will not record the results in the leaderboard.

### View the leaderboard

```bash
python mathcmder.py leaderboard [options]
```

Available options:

- `-o` or `--operation`: Filter the leaderboard by operation (+, -, *, /)
- `-n` or `--name`: Filter the leaderboard by name
- `-s` or `--sort`: Sort the leaderboard by score, count, time, or avg

Example usage:

```bash
python mathcmder.py leaderboard -o+ -n "Juan" -s count
```

This will display the leaderboard sorted by question count for the addition operation and only show the results of the user named "Juan".

```bash
python mathcmder.py leaderboard -s avg
```

This will display the leaderboard sorted by average time per question (best to worst).

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or PR on the [GitHub repository](https://github.com/znarfm/mathCMDer.git).

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/znarfm/mathCMDer/blob/main/LICENSE) file for more information.

---

Happy quizzing with MathCMDer!
