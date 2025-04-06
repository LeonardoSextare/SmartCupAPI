from fastapi import FastAPI

app = FastAPI()

@app.get("/soma")
def soma(a: float, b: float):
    return {"resultado": a + b}

