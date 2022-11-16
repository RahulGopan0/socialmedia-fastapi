from typing import List
from fastapi import status, HTTPException, APIRouter
from .. import schemas, utils, main


router = APIRouter(prefix="/users", tags=['Users'])

#Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser):
    hash = utils.hash(user.password)
    main.cursor.execute("""INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *""", 
                    (user.email, hash)) 
    new_user = main.cursor.fetchone()
    main.conn.commit() 
    return new_user


#Get Users
@router.get("/", response_model=List[schemas.UserResponse])
def get_users():
    main.cursor.execute(""" SELECT * FROM users """) 
    users = main.cursor.fetchall() 
    return users


#Get Specific User
@router.get("/{id}", response_model=schemas.UserResponse) 
def get_user(id: int): 
    main.cursor.execute("""SELECT * FROM users WHERE id = %s""", (id,))
    user = main.cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'User with ID {id} does not exist!')
    return user