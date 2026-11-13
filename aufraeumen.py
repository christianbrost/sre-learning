import argparse
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

CATEGORIES = {
    "bilder": [".jpg", ".jpeg", ".png"],
    "dokumente": [".pdf", ".txt"],
    "archive": [".zip", ".gz"],
}

def invert_categories(categories: dict[str, list[str]]) -> dict[str, str]:
    extension_to_category = {}
    logger.info("Initiating dictionary conversion from categories as keys to extensions")

    for category, extensions in categories.items():
        for extension in extensions:
            logger.info("Mapping %s -> %s", extension, category)
            extension_to_category[extension] = category

    return extension_to_category


def main():
    parser = argparse.ArgumentParser(description="move all files by extension into category folders")
    parser.add_argument("ordner", type=Path, help="folder that is being searched")
    parser.add_argument("-v", "--verbose", action="store_true", help="debug mode")
    parser.add_argument("-i", "--include-hidden", action="store_true", help="shows 'hidden' files")
    parser.add_argument("-d", "--dry-run", help="only lists changes that would be made")

    args = parser.parse_args()

    logging.basicConfig(
                level= logging.DEBUG if args.verbose else logging.INFO,
                format= "%(asctime)s %(levelname)-8s %(message)s"
    )

    ordner_path = args.ordner
    if not ordner_path.is_dir():
            parser.error(f"{ordner_path} ist kein Ordner")

    invert_categories(CATEGORIES)

if __name__ == "__main__":
    main()