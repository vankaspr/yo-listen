from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

class AccessToken(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    expire_at: int = 3600


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo_pool: bool = False
    echo: bool = False
    max_overflow: int = 50
    pool_size: int = 10
    
class GithubOauth(BaseModel):
    client_id: str
    client_secret: str
    redirect_uri: str = "http://localhost:8000/api/auth/github/callback"
    github_url: str = "https://github.com/login/oauth/access_token"
    github_email_url: str = "https://api.github.com/user/emails"
    github_user_url: str = "https://api.github.com/user"
    

class ApiPrefix(BaseModel):
    prefix: str = "/api"
    auth: str = "/auth"
    user: str = "/user"
    admin: str = "/admin"
    post: str = "/post"
    like: str = "/like"
    comment: str = "/comment"
    home: str = "/home"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_prefix="APP_CONFIG__",
        env_nested_delimiter="__",
    )
    
    
    api: ApiPrefix = ApiPrefix()
    access: AccessToken
    oauth: GithubOauth
    db: DatabaseConfig
    

settings = Settings()