from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #to tell passlib what is the hashing algorithm that we want to use which is, in this case, bcrypt

def hash(password: str):
    return pwd_context.hash(password)

def verify_pwd(password, password0):
    return pwd_context.verify(password, password0) #to verify both passwords are similar; password is plain str and password0 is a hash