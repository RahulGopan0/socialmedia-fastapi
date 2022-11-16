from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') #this is a dependancy which send eg: {"access_token": access_token, "token_type":"bearer"} to current_user(token)

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes #To give an expiration time for the token, case we can't let the user be logged in forever; 60 is 30min


def create_token(data: dict): #data stores the payload
    to_encode = data.copy()   #just a copy of data since we would wanto to manipulate it later
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #adding current time + 30min which is the token expiry
    to_encode.update({"exp": expiry})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #payload, secret_key, algorithm
    return encoded_jwt


def verify_token(token: str, cred_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #payload has the decoded token incl data in payload
        id: str = payload.get("user_id") #extracting the "user_id" from payload which we initially gave in the payload while making the token
        if id is None:
            raise cred_exception
        token_data = schemas.TokenData(id=id) #In this case, this literally returns the id with the var token_data since the payload only had id
    except JWTError: #This error occurs if the JSON Web Token (JWT) specified in the <Source> element of the Decode JWT policy is malformed, invalid or otherwise not decodable
        raise cred_exception
    return token_data


def current_user(token: str = Depends(oauth2_scheme)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                detail=f'Could not authenticate credentials', 
                                headers={"WWW-AUTHENTICATE": "Bearer"}) #WWW-Authenticate is an HTTP header that defines which HTTP Authentication scheme will be implemented to the resource. In this case, the authentication scheme used is bearer. Check tg to know about bearer
    #this function exists because when we return id with token_data, we could use that id here to find the user in our users db and send back the entire row instead of manually fetching user info at each end point; but we haven't implemented this here
    return verify_token(token, cred_exception)