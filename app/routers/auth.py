from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import utils, schemas, main, oauth2


router = APIRouter(tags=['Authentication'])


@router.post("/login", response_model=schemas.Token)
def user_login(user_cred: OAuth2PasswordRequestForm = Depends()): #depends() is a way for your code to declare things that it requires to work and use; example to declare any var type it
    main.cursor.execute("""SELECT password FROM users WHERE email = %s;""", 
                        (user_cred.username,)) 
    hash0 = main.cursor.fetchone()
    main.cursor.execute("""SELECT id FROM users WHERE email = %s;""", 
                        (user_cred.username,)) 
    id = main.cursor.fetchone()
    if not hash0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid credentials")
    hash0 = hash0["password"] #to extract the dict value and reassign it to hash0 since .verify() does not take dict as an input
    id = id["id"]
    if not utils.verify_pwd(user_cred.password, hash0): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Invalid credentials")
    token = oauth2.create_token(data={"user_id": id})
    return {"access_token": token, "token_type": "bearer"}