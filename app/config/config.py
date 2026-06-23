import os
from pathlib import Path
from dotenv import load_dotenv


# Definition of Root path for the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


#Load environment variables
load_dotenv(dotenv_path=ENV_PATH)


#Extract variables from .env file
class Settings:

    #Database settings
    DB_NAME=os.getenv("DB_NAME")
    DB_HOST=os.getenv("DB_HOST")
    DB_USER=os.getenv("DB_USER")
    DB_PASSWORD=os.getenv("DB_PASSWORD")
    DB_PORT=os.getenv("DB_PORT")

    
    def construct_db_url(self) -> str:

        DB_URL: str = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

        return DB_URL




settings=Settings()