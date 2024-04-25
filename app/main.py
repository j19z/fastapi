from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, posts, users, vote


# Now that we have alembic we dont really need this code, but im keeping it here for future reference.
#from . import models
#from .database import engine
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Use this is you want to allow cetain domains to access you API 
# origins = ['https://www.google.com']
# Use this if you want set a public API so anyone can access it use:
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(vote.router)


@app.get("/")
def read_root():
    return {'message': "Hellow Worlds"}
