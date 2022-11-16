from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .routers import users, posts, auth, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


while True:
    try: #we use try in py whenever we execute something that could fail. Connecting to a database could fail for multiple reasons
        conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name, user=settings.database_username, password=settings.database_password, cursor_factory=RealDictCursor)
        #this postgres driver sends back rows w/o column names; to get column names, we need to pass cursor_factory)
        cursor = conn.cursor() #this var will be used to execute SQL statements
        print("Database connection was successful")
        break #if connection is successful, we'll break out from the while loop; otherwise it will continue until connection is set
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(3) #To wait for 3sec until trying to reconnect


#def find_post(id):
#    for p in my_posts:
#        if p["id"] == id:
#            return p


#def find_index(id):
#    for i, p in enumerate(my_posts):
#        if p['id'] == id:
#            return i


app.include_router(posts.router) #when we send a HTTP request, this app object includes router which is in posts and looks for matching HTTP request there
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
