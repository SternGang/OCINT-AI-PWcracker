import os

possible_usernames = ["johnDoe", "DoeJohn",
"SocialPup7", "Eodnhoj",
"michaelscott", "TwitterJohn",
"johnDoe", "DogLover7", "Doeg"]

new_array = []

for entry in possible_usernames:
    if os.path.exists(f"results/{entry}.txt"):

        with open(f"results/{entry}.txt") as file:
            for temp in file:
                if temp.startswith("http"):
                    new_array.append(temp.replace('\\n', ''))

possible_usernames = new_array
for entry in possible_usernames:
    print(entry)
