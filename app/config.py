from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_hostname: str=os.getenv("DATABASE_HOSTNAME")
    database_port: str=os.getenv("DATABASE_PORT")
    database_password: str=os.getenv("DATABASE_PASSWORD")
    database_name: str=os.getenv("DATABASE_NAME")
    database_username: str=os.getenv("DATABASE_USERNAME")
    secret_key: str=os.getenv("SECRET_KEY")
    algorithm: str=os.getenv("ALGORITHM")
    access_token_expire_minutes: int=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    
settings = Settings()

# from pydantic_settings import BaseSettings, SettingsConfigDict
# class Settings(BaseSettings):
#     database_hostname: str
#     database_port: str
#     database_password: str
#     database_name: str
#     database_username: str
#     secret_key: str
#     algorithm: str
#     access_token_expire_minutes: int

#     model_config = SettingsConfigDict(env_file=".env")

# settings = Settings()