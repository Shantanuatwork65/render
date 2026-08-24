from fastapi import FastAPI

app=FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/items/")
def read_item(a: int, b: int):
    return {"a": a, "b": b, "sum": a + b}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)