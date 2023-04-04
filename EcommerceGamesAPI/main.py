import uvicorn
from fastapi import FastAPI
from games.routers import games_router

app = FastAPI()

app.include_router(games_router.router)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8001)
