from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    db_url: str = "sqlite:///padel_wizard.db"
    log_level: str = "INFO"
    env: str = "dev"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
print("TOKEN:", settings.bot_token)
