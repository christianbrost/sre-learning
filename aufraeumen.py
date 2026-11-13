import argparse
import logging
import shutil
from pathlib import Path
from inventar import list_files

logger = logging.getLogger(__name__)

CATEGORIES = {
    "bilder": [".jpg", ".jpeg", ".png"],
    "dokumente": [".pdf", ".txt"],
    "archive": [".zip", ".gz"],
}

FALLBACK_CATEGORY = "sonstiges"

def invert_categories(categories: dict[str, list[str]]) -> dict[str, str]:
    extension_to_category = {}

    for category, extensions in categories.items():
        for extension in extensions:
            logger.debug("Mapping %s -> %s", extension, category)
            extension_to_category[extension] = category

    return extension_to_category

def move_file(file: Path, target: Path, is_dry_run: bool):
    if is_dry_run:
        logger.info("[DRY-RUN] would move %s -> %s", file, target)
        return

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(file, target)
    logger.info("moved %s -> %s", file, target)
    
def main():
    parser = argparse.ArgumentParser(description="move all files by extension into category folders")
    parser.add_argument("folder", type=Path, help="folder that is being searched")
    parser.add_argument("-v", "--verbose", action="store_true", help="debug mode")
    parser.add_argument("-i", "--include-hidden", action="store_true", help="shows 'hidden' files")
    parser.add_argument("-d", "--dry-run", action="store_true", help="only lists changes that would be made")

    args = parser.parse_args()

    logging.basicConfig(
        level= logging.DEBUG if args.verbose else logging.INFO,
        format= "%(asctime)s %(levelname)-8s %(message)s"
    )

    folder_path = args.folder
    if not folder_path.is_dir():
        parser.error(f"{folder_path} is not a folder")

    logger.info("folder %s will be sorted", folder_path)

    is_dry_run = args.dry_run

    if is_dry_run:
        logger.info("Proceeding with dry run")

    extension_to_category = invert_categories(CATEGORIES)
    skipped = 0
    moved = 0

    for file in list_files(folder_path, args.include_hidden):
        category = extension_to_category.get(file.suffix.lower(), FALLBACK_CATEGORY)
        target = folder_path / category / file.name
        if target.exists():
            logger.warning("target exists, skipping: %s", target)            
            skipped += 1
            continue
        move_file(file, target, is_dry_run)
        moved += 1

    if is_dry_run:
        logger.info("Skipped %d, would move %d", skipped, moved)
    else:
        logger.info("Skipped %d, moved %d", skipped, moved)

if __name__ == "__main__":
    main()