from fastapi import FastAPI, Depends
from routers.memberRouter import memberRouter

app = FastAPI()
app.include_router(memberRouter)

@app.get("/")
def read_root():
    return {"Hello": "World"}