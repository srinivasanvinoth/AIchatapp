from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AWS_REGION: str = "ap-south-1"
    USERS_TABLE: str = "Users"
    CONVERSATIONS_TABLE: str = "Conversations"

    JWT_SECRET_KEY: str="tY75PxaWr2SSwRKCaThfiCINAaLInXZ0KhHMFMu22_YXQzMXBWS32tw1FJOd_bMwqqqoLowR1boHCcSmBh47bg"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    
    GEMINI_CHAT_MODEL: str = "gemini-2.5-flash"
    GEMINI_EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    PDF_TOP_K: int = 4

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
