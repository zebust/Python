import re

tempRegex = re.compile(r'''(
                       (?=.*[0-9])             # match atleast one digit
                       (?=.*[a-z])             # match atleast one  small letter
                       (?=.*[A-Z])             # match atleast one capital letter
                       (?=.*[@#$%_])           # match atleast one of these special charactor
                       .{8,})'''               # atleast 8 charactor long
                       ,re.VERBOSE)

txt = input()

result = tempRegex.match(txt)

if result:
    print("Valid password")
else:
    print("Invalid Password")


