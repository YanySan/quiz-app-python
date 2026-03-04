# Quiz App - Python Console Application

A console-based quiz application with **admin and contestant roles**, scoring, ranking, and lifelines (50-50 and Replace question).  

---

## Features

- Admin can:
  - Add new users
  - Delete users (cannot delete self or last admin)
  - Choose the active set of questions (set1.txt, set2.txt...). Original code was tested on 4 sets. 
- Contestants can:
  - Play quiz sets with **10 questions per set**
  - Use lifelines:
    - **50-50**: removes 2 wrong answers
    - **Replace**: swap a question with a backup question
    - **Rules**: Each lifeline can only be used **once per set**, even if used on the same question or on a replacement question.
  - Can play each set of questions only once (data stored in `active_set.txt`, created at runtime)
  - Check ranking list with scores
- The app tracks:
  - Which question sets each user has played (`user_sets.txt`, created at runtime)
  - Scores across multiple sessions (`rank_list.txt`, created at runtime)
- Ranking list shows users **sorted by number of correct answers**.

---

## Project Structure

- `main.py`                 — Main script to run the app  
- `Users.py`                — User class, login, user menus  
- `QuizQuestions.py`        — Quiz questions loading and game logic  
- `Users.txt`               — Stores user credentials (**ignored in git**). Uploaded version here contains example data (**format: username:password:role**)
- `set1.txt`                — Example question set (**format: numbered questions with a/b/c/d answers, last question reserved for Replace lifeline**)
- `rank_list.txt`           — Stores scores (**ignored in git**)  
- `user_sets.txt`           — Tracks which sets users have played (**ignored in git**)  
- `active_set.txt`          — Currently active question set (**ignored in git**)  
- `README.md`               — Project documentation  
- `LICENSE.md`              — MIT License  

---

## How to Run

1. Clone the repository  
2. Ensure you have **Python 3.x** installed  
3. Run the app in your console:
   ```bash
   python main.py
---


## Future Improvements
- GUI
- Client-server version
- Database integration
