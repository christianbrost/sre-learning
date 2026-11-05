from pathlib import Path
from collections import Counter

path = Path.cwd() / "testdaten"

suffixList = [] #list where all suffixes get added

for file in path.iterdir():
    if file.is_file():
        suffixList.append(file.suffix.lower())

c = Counter(suffixList)

for value, count in c.most_common():
    if value == "":
        print("(ohne Endung): ", count)
    else:
        print(value + ":", count)