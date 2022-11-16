from pydantic import BaseSettings

class Settings(BaseSettings): #To typecast and validate environment variables; when called, it will check the system for that env var, if not found it will give an error; we can also give a default value
    database_hostname: str #env var are normally written in all-caps but both can be used; pydantic makes sure the env var is case-insensitive
    database_port: int
    database_password: str
    database_username: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config: #To import env var from .env file
        env_file = ".env"

settings = Settings() #Instance of the class Settings(); we can now use settings to access these env var and values it hold