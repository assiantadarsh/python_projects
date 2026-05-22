'''
1 for snake
-1 for water
0 for gun
'''

import random

ran = random.randint(0, 2)

computerchoice = [1, -1, 0]
choice = computerchoice[ran]

user = input("Enter your choice s/w/g : ")

dict_choice = {"s": 1, "w": -1, "g": 0}
user_choice = dict_choice[user]

print("Computer choice:", choice)
print("Your choice:", user_choice)

if choice == user_choice:
    print("Draw!")

elif choice == -1 and user_choice == 1:
    print("You Win!❤️")

elif choice == 0 and user_choice == -1:
    print("You Win!❤️")

elif choice == 1 and user_choice == 0:
    print("You Win!❤️")

else:
    print("You Lose!🥲")