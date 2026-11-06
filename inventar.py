from pathlib import Path
from collections import Counter
import argparse

#path = Path.cwd() / "testdaten"




def listFileExtensions(path, includeHidden):
    suffixList = [] #list where all suffixes get added

    for file in path.iterdir():
        if file.is_file():
            if includeHidden and file.name.startswith("."):
                suffixList.append("hidden")
            else:
                if file.name.startswith("."):
                    continue
                else:
                    suffixList.append(file.suffix.lower())


    counterList = Counter(suffixList)
    printExtensionList(counterList)


#hidden files erkennen über file.name.startswith(".")
#empfehlung: standardmäßig überspringen

def printExtensionList(extensionListCounter):
    for value, count in extensionListCounter.most_common():
        if value == "":
            print("(ohne Endung):", count)
        else:
            print(value + ":", count)

def main():
    parser = argparse.ArgumentParser(description="Listet die Dateiendungen auf.")
    parser.add_argument("ordner", type=Path)
    parser.add_argument("-i", "--include-hidden", action="store_true", help="Zeigt 'hidden' Dateien")

    args = parser.parse_args()

    ordnerPath = args.ordner

    if not ordnerPath.is_dir():
        parser.error(f"{ordnerPath} ist kein Ordner")

    includeHidden = args.include_hidden


    listFileExtensions(ordnerPath, includeHidden)
    


if __name__ == "__main__":
    main()

