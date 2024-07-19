from fastapi import FastAPI
from util.database import init_db
from apis import auth, user, tasks



app = FastAPI()
# Define routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(tasks.router)

# intialize database
init_db()
