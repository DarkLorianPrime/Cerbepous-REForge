import asyncio

from routers.common.common import router as common_router
from routers.translate.translate import router as translate_router
from settings import settings
from vixengram.internationalization import i18n
from vixengram.routing import Router
from vixengram.core import VixenGram

app = VixenGram(token=settings.TG_TOKEN, i18n=i18n())
main_router = Router()


if __name__ == "__main__":
    main_router.include_router(common_router)
    main_router.include_router(translate_router)
    app.add_router(main_router)
    app.generate_api()
    asyncio.run(app.polling())
