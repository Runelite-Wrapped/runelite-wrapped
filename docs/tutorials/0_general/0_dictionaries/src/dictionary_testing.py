# friends = {"Jerome": "27", "Ryan": "26", "Jurgens": "27", "Nick": "31", "Will": "26"}
# friends["Nick"] = "32"
#
# del friends["Nick"]
#
# friends["Deb"] = 23
#
# print(friends)

string = "hello"
char_frequency = {}

for i in string:
    if i in char_frequency:
        char_frequency[i] += 1
    else:
        char_frequency[i] = 1

print(char_frequency)
