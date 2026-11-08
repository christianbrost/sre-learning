

def invert_categories(categories: dict[str, list[str]]) -> dict[str, str]:
    extension_to_category = {}

    for category, extensions in categories.items():
        for extension in extensions:
            extension_to_category[extension] = category

    return extension_to_category


def main():
    trial_map = {"bilder": [".jpg", ".jpeg", ".png"], "dokumente": [".pdf", ".txt"], "archive": [".zip", ".gz"]}

    #print(trialMap)
    print(invert_categories(trial_map))

if __name__ == "__main__":
    main()