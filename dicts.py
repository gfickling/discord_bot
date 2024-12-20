prompts = [
    "who",
    "what",
    "when",
    "where",
    "why",
    "how"
]

replies = [
    "Woah there",
    "This is not a drill",
    "You and whose army",
    "That's what she said",
    "In my past life, I was also an idiot",
    "Run in, go pants on fire",
    "It's not too late",
    "It's too late"
]

one_liners = [
    "I hate Russian dolls, they're so full of themselves.",
    "I asked my North Korean friend how it was there, he said he couldn't complain.",
    "My girlfriend started smoking, so I slowed down and applied Lubricant.",
    "I, for one, like Roman numerals.",
    "My wife told me to stop impersonating a flamingo. I had to put my foot down.",
    "My wife and I were happy for twenty years; then we met.",
    "I haven't slept for three days, because that would be too long.",
    "The first time I got a universal remote control, I thought to myself 'This changes everything.'",
    "My grandfather has the heart of a lion and a lifetime ban from the local zoo.",
    "My friend gave me his Epi-Pen as he was dying. It seemed very important to him that I have it.",
    "I've spent the past four years looking for my ex-girlfriend's killer, but no one will do it.",
    "I saw a sign that said 'watch for children' and I thought, 'That sounds like a fair trade.'",
    "I refused to believe my road worker father was stealing from his job, but when I got home, all the signs were there.",
    "I recently decided to sell my vacuum cleaner, all it was doing was gathering dust.",
    "People say I'm condescending. That means I talk down to people that can't understand simple shit like the word condescending.",
    "You can never lose a homing pigeon - if your homing pigeon doesn't come back, what you've lost is a pigeon.",
    "Whiteboards are remarkable.",
    "I was at an ATM and this old lady asked me to help check her balance, so I pushed her over."
]

paraprosdokians = [
    "Where there's a will, I want to be in it.",
    "The last thing I want to do is hurt you, but it's still on my list.",
    "Since light travels faster than sound, some people appear bright until you hear them speak.",
    "If I agreed with you, we'd both be wrong.",
    "War does not determine who is right - only who is left.",
    "Knowledge is knowing a tomato is a fruit. Wisdom is not putting it in a fruit salad.",
    "They begin the evening news with 'Good Evening,' then proceed to tell you why it isn't.",
    "To steal ideas from one person is plagiarism. To steal from many is research.",
    "I thought I wanted a career. Turns out, I just wanted pay checks.",
    "In filling out an application, where it says, 'In case of emergency, notify:' I put 'DOCTOR.'",
    "I didn't say it was your fault, I said I was blaming you.",
    "Women will never be equal to men until they can walk down the street...with a bald head and a beer gut, and still think they are sexy.",
    "Behind every successful man is his woman. Behind the fall of a successful man is usually another woman.",
    "A clear conscience is the sign of a fuzzy memory.",
    "You do not need a parachute to skydive. You only need a parachute to skydive twice.",
    "Money can't buy happiness, but it sure makes misery easier to live with.",
    "There's a fine line between cuddling and...holding someone down so they can't get away.",
    "I used to be indecisive. Now I'm not so sure.",
    "You're never too old to learn something stupid.",
    "To be sure of hitting the target, shoot first and call whatever you hit the target.",
    "Nostalgia isn't what it used to be.",
    "Change is inevitable, except from a vending machine.",
    "Going to church doesn't make you a Christian any more than standing in a garage makes you a car.",
    "I'm supposed to respect my elders, but now it's getting harder and harder for me to find one."
]

lists = {'prompts': prompts, 'replies': replies, 'one_liners': one_liners, 'paras': paraprosdokians}

import json

def write_to_file(name, contents):
    try:
        with open(f"data/{name}.py","x") as f:
            f.write(name + ' = ')
            f.write('[\n    ')
            index = 1
            last = len(contents)
            for line in contents:
                if index == last:
                    f.write(json.dumps(line))
                    f.write('\n]\n\n')
                    continue
                f.write(json.dumps(line))
                f.write(',\n    ')
                index += 1
    except FileExistsError:
        print(f"data/{name}.py already exists")
        with open(f"data/{name}.py","a") as f:
            f.write(name + ' = ')
            f.write('[\n    ')
            index = 1
            last = len(contents)
            for line in contents:
                if index == last:
                    f.write(json.dumps(line))
                    f.write('\n]\n\n')
                    continue
                f.write(json.dumps(line))
                f.write(',\n    ')
                index += 1
    try:
        with open("data/database.py","x") as f:
            f.write(name + ' = ')
            f.write('[\n    ')
            index = 1
            last = len(contents)
            for line in contents:
                if index == last:
                    f.write(json.dumps(line))
                    f.write('\n]\n\n')
                    continue
                f.write(json.dumps(line))
                f.write(',\n    ')
                index += 1
    except FileExistsError:
        print("data/database.py already exists")
        with open("data/database.py","a") as f:
            f.write(name + ' = ')
            f.write('[\n    ')
            index = 1
            last = len(contents)
            for line in contents:
                if index == last:
                    f.write(json.dumps(line))
                    f.write('\n]\n\n')
                    continue
                f.write(json.dumps(line))
                f.write(',\n    ')
                index += 1



def create_list_of_dicts(name, list_data):
    to_import = []
    for item in list_data:
        temp_dict = {}
        temp_dict[f'{name}'] = item
        to_import.append(temp_dict)
    return to_import

for k, v in lists.items():
    write_to_file(k, create_list_of_dicts(k, v))