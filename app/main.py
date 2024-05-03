from fastapi import FastAPI

app = FastAPI()


@app.get("/hello-world")
async def root() -> str:
    return 'Hello World!'
