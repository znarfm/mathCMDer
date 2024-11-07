# MathCMDer 🧮

## Description

MathCMDer is a command-line interface (CLI) math quiz application written in Python that helps users practice their arithmetic skills through interactive questions. It features customizable difficulty levels, various operations, and a local leaderboard system to track progress.

This project was developed as part of the [CS50P](https://cs50.harvard.edu/python/) course requirements.

## 🚀 Features

- **Customizable Quiz Settings**
  - Choose number of questions
  - Select operation type (addition, subtraction, multiplication, or division)
  - Set custom operand ranges
  - Optional timer for each question
  
- **Performance Tracking**
  - Local leaderboard using SQLite
  - Track scores, completion time, and average response time
  - Filter and sort leaderboard results

## 🛠️ Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/znarfm/mathCMDer.git
cd mathCMDer
```

2. Create and activate a virtual environment:

**Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📖 Usage

### Starting a Quiz

Basic command structure:
```bash
python mathcmder.py start [options]
```

#### Required Options:
- `-c, --count NUMBER_OF_QUESTIONS` - Set number of questions
- `-o, --operation {+,-,*,/}` - Choose arithmetic operation

#### Optional Parameters:
- `-l, --lowest LOWEST_OPERAND` - Set minimum operand value (default: 1)
- `-m, --max HIGHEST_OPERAND` - Set maximum operand value (default: 10)
- `-t, --timer SECONDS` - Set question timeout in seconds
- `-n, --name NAME` - Set player name for leaderboard
- `-nl, --no-leaderboard` - Opt out of leaderboard recording

#### Examples:

Basic addition quiz:
```bash
python mathcmder.py start -c 10 -o+
```

Timed multiplication quiz with custom range:
```bash
python mathcmder.py start -c 15 -o* -l 2 -m 12 -t 5 -n "Player1"
```

### Viewing the Leaderboard

Basic command structure:
```bash
python mathcmder.py leaderboard [options]
```

#### Available Options:
- `-o, --operation {+,-,*,/}` - Filter by operation
- `-n, --name NAME` - Filter by player name
- `-s, --sort {score,time,count,avg}` - Sort results

#### Examples:

View all scores:
```bash
python mathcmder.py leaderboard
```

Filter multiplication scores for a specific player:
```bash
python mathcmder.py leaderboard -o* -n "Player1" -s score
```

## 🧪 Testing

*Coming soon: Information about running tests and test coverage*

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

Please ensure your PRs include appropriate documentation and test coverage.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/znarfm/mathCMDer/blob/main/LICENSE) file for details.

## 🙏 Acknowledgments

- CS50P course team for the project inspiration
- Contributors and users of the project

---

📫 For bug reports and feature requests, please [open an issue](https://github.com/znarfm/mathCMDer/issues).

Happy quizzing with MathCMDer! 🎯