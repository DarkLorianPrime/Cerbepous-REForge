from settings import settings


def url_compiler(method):
    return f'{settings.API_URL}/bot{settings.TG_TOKEN}/{method}'
