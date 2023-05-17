from fastapi import FastAPI


app = FastAPI()


_SAMPLE_DATA = [
    {
        "image": "https://oldschool.runescape.wiki/images/Hans.png?1a5c5",
        "text": "You've played for:<br /> 2080 hours<br />That's a full working year!",
    },
    {
        "image": "https://oldschool.runescape.wiki/images/Goblin.png?3e49a",
        "text": "Your most killed mob is:<br />Goblin (lvl 3)<br />with 42069 kills!",
    },
    {
        "image": "https://oldschool.runescape.wiki/images/Grand_Exchange_pillar.png?90523",
        "text": "Your favourite location is:<br />The Grand Exchange<br />with 703 visits<br />Totalling 803 hours!",
    },
    {
        "image": "https://oldschool.runescape.wiki/images/Rock_golem_%28follower%29.png?269fc",
        "text": "Your favourite skill is:<br />Mining<br />with 42069 xp gained",
    },
]


@app.get("/api/v1/wrapped")
async def wrapped(username: str) -> list:
    # append username to each dict's text
    return [
        {
            "image": item["image"],
            "text": f"{username} {item['text']}",
        }
        for item in _SAMPLE_DATA
    ]
