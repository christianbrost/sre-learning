from pathlib import Path
from collections import Counter
import argparse

import logging
import shutil

logger = logging.getLogger(__name__)

def count_extensions(folder: Path, include_hidden: bool) -> Counter[str]:
    suffix_list = [] 

    for file in folder.iterdir():
        if not file.is_file():
            logger.debug("skipping sub folder '%s'", file.name)
            continue
        if file.name.startswith("."):
            if not include_hidden:
                logger.debug("skip hidden file %s", file.name)
                continue
            suffix_list.append("hidden")
            logger.debug("appended hidden file %s", file.name)
            continue
        logger.debug("add %s to counter as %s", file.name, file.suffix if file.suffix != "" else "(no extension)")
        suffix_list.append(file.suffix.lower())

    return Counter(suffix_list)

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

    extension_count = count_extensions(ordner_path, args.include_hidden)

    list_length = sum(extension_count.values())

    logger.info("Found %s files", list_length)

    print_extension_list(extension_count)

if __name__ == "__main__":
    main()
