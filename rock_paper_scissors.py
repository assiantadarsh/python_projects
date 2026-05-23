'''
1 for Rock
-1 for Paper
0 for Scissor
'''
print("You are playing Rock Paper and Scissors!")

import random
continue_game = True
while(continue_game):
    ran = random.randint(0, 2)

    computerchoice = [1, -1, 0]
    choice = computerchoice[ran]

    user = input("Enter your choice R/P/S : ").upper()

    dict_choice = {"R": 1, "P": -1, "S": 0}

    if user not in dict_choice:
        print("Invalid choice! Please enter only R, P, or S.")
    else:
        user_choice = dict_choice[user]

    print("Computer choice:", choice)
    print("Your choice:", user_choice)

    if choice == user_choice:
        print("Draw!")

    elif choice == 1 and user_choice == -1:
        print("You Win!❤️")

    elif choice == -1 and user_choice == 0:
        print("You Win!❤️")

    elif choice == 0 and user_choice == 1:
        print("You Win!❤️")

    else:
        print("You Lose!🥲")

    c = input("Continue playing yes/no : ").lower()
    if(c == 'yes'):
        continue_game = True
    else:
        continue_game = False
        print("ThakYou For Playing!❤️")

