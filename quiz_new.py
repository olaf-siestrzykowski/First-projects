def new_game():
    guesses = []
    correct_guesses = 0
    question_num = 1
    for key in questions:
        print("--------------------------")
        print(key)
        for i in options[question_num-1]:
            print(i)
        guess = input("Enter (A, B, C or D): ").upper()
        guesses.append(guess)

        correct_guesses += check_answer(questions.get(key),guess)
        question_num +=1

    display_score(correct_guesses,guesses)
#-----------------------------------------
def check_answer(answer, guess):
    if answer == guess:
        print("Correct!")
        return 1
    else:
        print("Wrong!")
        return 0
#-----------------------------------------
def display_score(correct_guesses, guesses):
    print("------------------")
    print("Results")
    print("------------------")
    print("Answers: ", end=" ")
    for i in questions:
        print(questions.get(i), end=" ")
    print()

    print("Guesses: ", end=" ")
    for i in guesses:
        print(i, end=" ")
    print()

    score = int((correct_guesses/len(questions))*100)
    print("Your score is: "+str(score)+"%")
#-----------------------------------------
def play_again():
    response = input("Do you want to play again? (yes/no): ").upper()
    if response == "YES":
        return True
    else:
        return False
#-----------------------------------------

questions = {
    "How often does Oli dance?: ": "B",
    "What time does Oli wake up?: ": "C",
    "What is Oli's favourite style?: ": "A",
    "What is Oli's favourite game?: ": "D",
}

options = [["A. few times a week", "B. everyday", "C. Oli does not dance", "D. once a week"],
           ["A. 7:00", "B. 10:00", "C. 8:30", "D. 5:00"],
           ["A. Popping", "B. Breaking", "C. Hip Hop", "D. House"],
           ["A. Gothic", "B. Crash Team Racing", "C. Naruto Ninja Storm", "D. Hinokami Chronicles"]]

new_game()

while play_again():
    new_game()

print("Bye!")