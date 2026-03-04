import random

class QuizQuestions:
    def __init__(self, question_text, answers, correct):
        self.question_text = question_text
        self.answers = answers
        self.correct = correct


def load_questions(filename):
    questions = [] #list for saving questions
    current_question = "" #current question we read
    answers = {} #dict for saving answers for current question

    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # loop to read each line of the file
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line[0].isdigit():
            if current_question: #checking if we had any previous question saved
                questions.append(create_question(current_question, answers))
                answers = {}
            current_question = line[3:].strip()

        elif line[0] in ["a", "b", "c", "d"]:
            answers[line[0]] = line[3:].strip()

    if current_question: #for the last question, we have to extract it separately
        questions.append(create_question(current_question, answers))

    return questions
    # Returning the list of all questions


def create_question(question_text, answers):
    #creating object of the class with correct answer option and shuffled answer options
    items = list(answers.items())
    random.shuffle(items)

    new_answers = {}
    correct_key = None
    keys = ["a", "b", "c", "d"]

    for i, (old_key, value) in enumerate(items):
        new_answers[keys[i]] = value
        if old_key == "d":
            correct_key = keys[i]

    return QuizQuestions(question_text, new_answers, correct_key)
    #returning class object with new answer options (randomized) and correct one marked


def questions_set():
#asking admin to choose the active set of questions, and writes that option in the file active_set.txt
    while True:
        x = input("Choose the active set of questions (1-4): ")

        if x.isdigit() and 1 <= int(x) <= 4:
            filename = f"set{x}.txt"
            print(f"The set {x} of questions is active.")

            with open("active_set.txt", "w") as f:
                f.write(filename)
            break
        else:
            print("Invalid input, try again")

    return filename
    #Returning the name of the active set

def play_quiz(user):
    # Load the active set
    try:
        with open("active_set.txt", "r") as f:
            filename = f.read().strip()
    except FileNotFoundError:
        print("No active question set selected by admin.")
        return

    # Check if the player has already played this set
    try:
        with open("user_sets.txt", "r") as f:
            played_sets = {}
            for line in f:
                line = line.strip()
                if line:
                    uname, uset = line.split(":")
                    played_sets.setdefault(uname, []).append(uset)
    except FileNotFoundError:
        played_sets = {}

    if filename in played_sets.get(user.username, []):
        print(f"You have already played this set. Please wait for a new active set.")
        return

    # Load questions from the file
    questions = load_questions(filename)
    if not questions:
        print("No questions found in this set.")
        return

    score = 0
    total_questions = len(questions) - 1  # last question is reserved for REPLACE lifeline
    print(f"\nStarting quiz (Total questions: {total_questions})\n")

    # Lifeline flags per set
    used_replace = False
    used_5050 = False

    for i, q in enumerate(questions[:-1], start=1):  # play original questions only
        print(f"Question {i}: {q.question_text}")
        for key in ["a","b","c","d"]:
            print(f"{key}) {q.answers[key]}")

        # Flags for lifeline usage per question
        question_done = False
        current_q = q

        while not question_done:
            prompt = "Your answer (a/b/c/d)"
            if not used_replace or not used_5050:
                prompt += " or use lifeline ('replace', '5050')"
            prompt += ": "
            ans = input(prompt).lower()

            # 50-50 lifeline
            if ans == "5050" and not used_5050:
                used_5050 = True
                wrong_keys = [k for k in current_q.answers if k != current_q.correct]
                removed = random.sample(wrong_keys, 2)
                print("\nRemaining answers:")
                for k in ["a","b","c","d"]:
                    if k not in removed:
                        print(f"{k}) {current_q.answers[k]}")
                continue  # allow player to answer after 50-50

            # Replace lifeline
            if ans == "replace" and not used_replace:
                used_replace = True
                current_q = questions[-1]  # use last question as replacement
                print(f"\nReplace Question: {current_q.question_text}")
                for key in ["a","b","c","d"]:
                    print(f"{key}) {current_q.answers[key]}")
                continue  # allow player to answer replacement question

            # Normal answer input
            if ans in ["a","b","c","d"]:
                if ans == current_q.correct:
                    print("Correct!\n")
                    score += 1
                else:
                    print(f"Wrong! Correct answer is: {current_q.correct}\n")
                question_done = True
            else:
                print("Invalid input, try again.")

        # Progress display
        print(f"Progress: {i}/{total_questions} questions answered.\n")

    # Update rank list and mark set as played
    save_score(user.username, score, total_questions)
    with open("user_sets.txt","a") as f:
        f.write(f"{user.username}:{filename}\n")

    print(f"{user.username} 🎉 Quiz finished! You scored {score}/{total_questions} correct answers.\n")


def save_score(username, score, total):
    results = []

    try:
        with open("rank_list.txt", "r") as file: #writing or updating score in file
            for line in file:
                line = line.strip()
                if line:
                    name, s, t = line.split(",")
                    results.append((name, int(s), int(t)))
    except FileNotFoundError:
        pass

    updated = False
    for i in range(len(results)):
        if results[i][0] == username:
            # Sum of current and previous points of the player
            new_score = results[i][1] + score
            new_total = results[i][2] + total
            results[i] = (username, new_score, new_total)
            updated = True
            break

    if not updated:
        results.append((username, score, total))

    with open("rank_list.txt", "w") as file:
        for name, s, t in results:
            file.write(f"{name},{s},{t}\n")


def show_ranking():
    try:
        with open("rank_list.txt", "r") as f:
            data = []

            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    name, score, total = line.split(",")
                    score = int(score)
                    total = int(total)
                    data.append((name, score, total))
                except ValueError:
                    continue  # skip broken lines

            # Sort by greatest number of correct answers (score), descending
            data.sort(key=lambda x: x[1], reverse=True)

    except FileNotFoundError:
        data = []

    print("\n--- Rank list ---")
    if not data:
        print("No results yet.")
    else:
        for i, (name, score, total) in enumerate(data, start=1):
            print(f"{i}. {name}: {score}/{total}")
    print("-----------------\n")