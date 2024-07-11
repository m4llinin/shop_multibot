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


async def load_infobase():
    js = asyncj.AsyncJson("infobase.json")
    return await js.read()


async def write_infobase(key: str, value: str = None):
    infobase = await load_infobase()

    if value is None:
        infobase.pop(key)
    else:
        infobase[key] = value

    js = asyncj.AsyncJson("infobase.json")
    return await js.write(infobase)
