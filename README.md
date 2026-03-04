# Quiz App - Python Console Application

A console-based quiz application with **admin and contestant roles**, scoring, ranking, and lifelines (50-50 and Replace question).  

---

## Features

- Admin can:
  - Add new users
  - Delete users (cannot delete self or last admin)
  - Choose the active set of questions
- Contestants can:
  - Play quiz sets with **10 questions per set**
  - Use lifelines:
    - **50-50**: removes 2 wrong answers
    - **Replace**: swap a question with a backup question
    - **Rules**: Each lifeline can only be used **once per set**, even if used on the same question or on a replacement question.
  - Check ranking list with scores
- The app tracks:
  - Which question sets each user has played
  - Scores across multiple sessions
- Ranking list shows users **sorted by number of correct answers**.

---

## How to Run
1. Clone repository
2. Run `python main.py`

## Future Improvements
- GUI
- Client-server version
- Database integration
