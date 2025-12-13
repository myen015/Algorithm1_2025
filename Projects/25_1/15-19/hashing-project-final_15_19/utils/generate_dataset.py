import random

kazakh_letters = "қөңәұүңғқғқабвгдеёжзийклмнопрстуфхцчшщьыәөұүқғң"
latin_letters = "abcdefghijklmnopqrstuvwxyz"

def gen_kazakh_word(length):
    return "".join(random.choice(kazakh_letters) for _ in range(length))

def gen_english_word(length):
    return "".join(random.choice(latin_letters) for _ in range(length))

def gen_random_string():
    charset = latin_letters + "0123456789"
    return "".join(random.choice(charset) for _ in range(12))


def generate():
    with open("data/kazakh_synthetic.txt", "w", encoding="utf-8") as f:
        for _ in range(20000):
            f.write(gen_kazakh_word(random.randint(3, 8)) + "\n")

    with open("data/english_synthetic.txt", "w") as f:
        for _ in range(20000):
            f.write(gen_english_word(random.randint(3, 10)) + "\n")

    with open("data/random_synthetic.txt", "w") as f:
        for _ in range(30000):
            f.write(gen_random_string() + "\n")

    print("Datasets generated successfully!")

if __name__ == "__main__":
    generate()
