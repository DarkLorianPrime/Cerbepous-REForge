from vixengram.settings import settings


def url_compiler(method: str) -> str:
    return f"{settings.api_url}/bot{settings.TG_TOKEN}/{method}"
