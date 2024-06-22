import asyncj


async def load_texts(language: str = 'ru'):
    js = asyncj.AsyncJson("texts.json")
    texts = await js.read()
    return texts.get(language, texts['ru'])


async def load_settings():
    js = asyncj.AsyncJson("./config/settings.json")
    return await js.read()


async def write_settings(**kwargs):
    shop = await load_settings()
    for k, v in kwargs.items():
        shop[k] = v

    js = asyncj.AsyncJson("./config/settings.json")
    return await js.write(shop)
