import asyncio
from os import getenv

from routers.common.common import router as common_router
from routers.translate.translate import router as translate_router
from routers.help_menu.help import router as help_router
from settings import settings
from vixengram.internationalization import i18n
from vixengram.routing import Router
from vixengram.core import VixenGram

app = VixenGram(
    title="Cerberous",
    version="1.0.0-alpha",
    token=settings.TG_TOKEN,
    i18n=i18n()
)
main_router = Router()

if __name__ == "__main__":
    main_router.include_router(common_router)
    main_router.include_router(translate_router)
    main_router.include_router(help_router)
    app.add_router(main_router)
    json_api = app.generate_api()
    asyncio.run(
        app.webhook(
            webhook_url=getenv("webhook_url", ""),
            host="0.0.0.0",
            port=8090,
            api_schema=json_api
        )
    )
