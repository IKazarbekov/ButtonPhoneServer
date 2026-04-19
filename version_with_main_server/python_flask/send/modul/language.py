def get_words(word: str) -> tuple[str, str]:
    with open("data/language_words.txt", "r") as file:
        for line in file:
            words = line.strip().split(";")
            if words[0] == word:
                return ("Русский: " + words[1], "Башкирский: " + words[2])
            if words[1] == word:
                return ("Английский: " + words[0], "Башкирский: " + words[2])
            if words[2] == word:
                return ("Английский: " + words[0], "Русский: " + words[1])
    raise IndexError("word not found in dictionary for translate.")