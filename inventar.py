from pathlib import Path
from collections import Counter
import argparse

#path = Path.cwd() / "testdaten"




def count_extensions(folder: Path, include_hidden: bool) -> Counter[str]:
    suffixList = [] #list where all suffixes get added

    for file in folder.iterdir():
        if not file.is_file():
            continue
        if file.name.startswith("."):
            if not include_hidden:
                continue
            suffixList.append("hidden")
            continue
        suffixList.append(file.suffix.lower())

    return Counter(suffixList)


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

    extension_count = count_extensions(ordnerPath, includeHidden)
    
    printExtensionList(extension_count)

if __name__ == "__main__":
    main()

