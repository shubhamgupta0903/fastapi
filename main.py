from fastapi import FastAPI

app=FastAPI()


@app.get("/")

def hello():
    return "Hello World"

@app.get("/json_format")

def json():
    return {"heloo":{"intro":"i am shubham"}}
