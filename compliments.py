import random
import string


def flatten(x):
    for child in x:
        if iterable_except_string(child):
            for grandchild in flatten(child):
                yield grandchild
        else:
            yield child


def weighted(choices):
    total = sum(weight for weight, choice in choices)
    r = random.uniform(0, total)
    upto = 0
    for weight, choice in choices:
        if upto + weight > r:
            return choice
        upto += weight
    # we shouldn't get here, but just in case
    random.choice([choice for weight, choice in choices])


def iterable_except_string(x):
    return hasattr(x, '__iter__')


def terminate(x):
    if iterable_except_string(x):
        return flatten([terminate(child) for child in x])
    elif hasattr(x, '__call__'):
        return terminate(x())
    else:
        return x


def generate_text(start):
    return string.join(terminate(start), '')


def root():
    return weighted([
        (1, random.choice(compliments)),
        (0.05, ["DAMN GRRRL, ", random.choice(compliments)])
    ])


def get_compliment():
    return generate_text(root)


positives = [
    "pretty",
    "sexy",
    "cool",
    "fly",
    "dope",
    "smashing",
    "dashing",
    "fancy",
    "cute",
    "fierce",
    "brilliant"
]

compliments = [
    lambda: "you look like " + random.choice([
        "an ancient goddess",
        "a terrifying warrior",
        "the smartest person I've ever met",
        "a unicorn made of glitter and sparkles"]),
    lambda: random.choice([
        "I want to",
        "let me"]) +
    " " +
    random.choice([
        "braid your hair",
        "objectify you",
        "paint your picture",
        "hold your purse",
        "do your taxes for you",
        "stalk you in the most non-creepy way",
        "do all your chores", 
        "send you presents", 
        "make your life even more fabulous"]),
    lambda: "I would " + random.choice([
        "cut down a thousand trees",
        "murder",
        "knit a pair of socks", 
        "go to a family reunion"]) + " for you",
    lambda: "you are " + random.choice([
        "fierce and strange",
        "a heartbreaker",
        "more attractive than everyone you went to high school with",
        "more attractive than all of Instagram"
        "so cool"]),
    lambda: random.choice([
        "you look",
        "why are you so"]) + " " + random.choice(positives),
    lambda: "you deserve " + random.choice([
        "a raise",
        "free wifi",
        "freshly baked cookies", 
        "magic and mystery", 
        "sunshine and kisses", 
        "fan girls and boys", 
        "an internet community dedicated to respectfully appreciating your beauty",
        "free healthcare", 
        "a massage", 
        "all the cookies in the world", 
        "respect, adoration and love"]),
    "your eyes are like the tip of a unicorn horn",
    "your body is full of magic and sparkles",
    "a thousand puppies wouldn't be as cute as you",
    "your face is so pretty",
    "can we hang out and be best friends",
    "you are shiny and beautiful like a diamond",
    "you are working that outfit",
    "you are more beautiful than the entire royal family",
    "you look really smart",
    "your style is off the charts",
    "you are rocking your gender presentation",
    "can we get friendship bracelets and tell each other secrets",
    "your online presence is fierce",
    "you were probably the cutest baby",
    "you are definitely not a sidekick",
    "your face would make angels weep",
    "you'd have a sexy patronus"
    "you are more attractive to me than my anti-anxiety meds", 
    "you are the most clever person", 
    "i can't decide if i want to be you or be your best friend", 
    "i would pick you for fantasy football even if you were the worst player"
    "i always want you on my team", 
    "you could turn water into wine", 
    "i want to fall asleep staring into your eyes", 
    "if you said jump, i'd ask how high", 
    "all my friends think you're cooler than me", 
]
