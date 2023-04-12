import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from games.routers import games_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(games_router.router)


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8001)
