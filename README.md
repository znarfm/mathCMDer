# MathCMDer

## Video Demo: Coming Soon

## Description

MathCMDer is a command-line interface (CLI) math quiz application written in Python. It allows users to test their math skills by answering a series of arithmetic questions.

This is a project for [CS50P](https://cs50.harvard.edu/python/).

### Features

- Customizable number of questions
- Choose from addition, subtraction, multiplication, or division operations
- Set a range of operand values
- Optional timer for each question
- Local leaderboard

### Installation

Make sure you have Python 3.6 or higher installed to run this program.

1. Clone the repository

```bash
git clone https://github.com/znarfm/mathCMDer.git
```

2. Navigate to the project directory

```bash
cd mathCMDer
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage

To start the math quiz, run the following command:

```bash
python mathcmder.py start -c <number_of_questions> -o <operation> -l <lowest_value> -m <highest_value> -t <timeout> -n <name>
```

Replace the placeholders with the desired values:

- `<number_of_questions>` (required): The number of questions you want to answer.
- `<operation>` (required): The arithmetic operation you want to quiz(`+` for addition, `-` for subtraction, `*` for multiplication).
- `<lowest_value>` (defaults to `1`): The lowest possible value for the operands.
- `<highest_value>` (defaults to `10`): The highest possible value for the operands.
- `<timeout>`: Set a timeout (in seconds) for each question. If not specified, there will be no timeout.
- `<name>` (defaults to `Anonymous`): Name to be saved in the leaderboard.

Example usage:

Both are essentially the same. These will start a math quiz with 10 addition questions, using operands from 1 to 10, and a timeout of 5 seconds for each question. Since there is no `--name` flag given, the default name in the leaderboard will appear as `Anonymous`.

```bash
python mathcmder.py start --count 10 --operation + --lowest 1 --max 10 --timer 5
```

```bash
python mathcmder.py start -c10 -o+ -l1 -m10 -t5
```

This will start the program with 15 division questions, using the default operand values without a timeout, and the name `Juan` will appear in the leaderboard.

```bash
python mathcmder.py start -c15 -o/ -n "Juan"
```

To view the leaderboard values, use the `leaderboard` command:

```bash
python mathcmder.py leaderboard
```

## To-do

- [ ] Improve leaderboard (add sorting flags/arguments)
- [ ] Add flag to opt out in leaderboards
- [ ] Convert to object-oriented

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or PR on the [GitHub repository](https://github.com/znarfm/mathCMDer.git).

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/znarfm/mathCMDer/blob/main/LICENSE) file for more information.

---

Happy quizzing with MathCMDer!
