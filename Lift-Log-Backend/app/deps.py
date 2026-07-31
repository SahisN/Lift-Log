from settings import Settings, get_settings


def inject_app_settings() -> Settings:
    return get_settings("config.yaml")
