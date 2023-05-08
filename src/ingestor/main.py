from fastapi import FastAPI

app = FastAPI()


@app.post("/api/v1/event/game-tick/")
async def game_tick(event: dict):
    print(event)
    return {"message": "OK"}
