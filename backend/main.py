from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_router
from news.interface.controllers.news_controller import router as news_router
from containers import Container
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.container = Container()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000"],
	allow_credentials=True,
	allow_methods=["GET", "POST"],
	#TODO: 필요한 헤더만 넣어야 함
	allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(news_router)

@app.get("/")
def hello():
	return {"Hello": "World"}
