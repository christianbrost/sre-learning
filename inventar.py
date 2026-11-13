from pathlib import Path
from collections import Counter
import argparse

import logging

logger = logging.getLogger(__name__)

def list_files(folder: Path, include_hidden: bool) -> list[Path]:
    files = [] 

    for file in folder.iterdir():
        if not file.is_file():
            logger.debug("skipping sub folder '%s'", file.name)
            continue
        if file.name.startswith("."):
            if not include_hidden:
                logger.debug("skip hidden file %s", file.name)
                continue
            files.append(file)
            logger.debug("appended hidden file %s", file.name)
            continue
        logger.debug("adding file %s to file_list", file.name)
        files.append(file)

    return files

def count_extensions(files: list[Path]) -> Counter[str]:
    extension_list = []

    for file in files:
        if file.name.startswith("."):
            extension_list.append("hidden")
            continue
        extension_list.append(file.suffix.lower())

    return Counter(extension_list)

def print_extension_list(extension_list_counter):
    for value, count in extension_list_counter.most_common():
        if value == "":
            print(f"(no extension): {count}")
        else:
            print(f"{value}: {count}")

def main():

    parser = argparse.ArgumentParser(description="lists all suffixes with count")
    parser.add_argument("ordner", type=Path, help="folder that is being searched")
    parser.add_argument("-i", "--include-hidden", action="store_true", help="shows 'hidden' files")
    parser.add_argument("-v", "--verbose", action="store_true", help="debug mode")

    args = parser.parse_args()

    logging.basicConfig(
            level= logging.DEBUG if args.verbose else logging.INFO,
            format= "%(asctime)s %(levelname)-8s %(message)s"
        )

    ordner_path = args.ordner

    if not ordner_path.is_dir():
        parser.error(f"{ordner_path} ist kein Ordner")

    
    logger.info("folder added: '%s'", ordner_path)

    extension_count = count_extensions(list_files(ordner_path, args.include_hidden))

    list_length = sum(extension_count.values())

    logger.info("Found %s files", list_length)

    print_extension_list(extension_count)

if __name__ == "__main__":
    main()
