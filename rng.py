import random

def roll():
    rn = random.randint(100, 1000) / 100

    modifier = rn % 1
    modifier = modifier / 2
    modifier = modifier + 1

    t = int(rn)

    if 0 <= t <= 3:
        t = 5
    elif 4 <= t <= 5:
        t = 10
    elif 6 <= t <= 7:
        t = 15
    elif 8 <= t <= 9:
        t = 25
    else:
        t = 30

    finalt = t * modifier

    return {
        "final": round(finalt, 2),
        "base": t,
        "roll": round(rn, 2),
        "modifier": round(modifier, 2),
    }
