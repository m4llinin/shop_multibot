import asyncj


async def load_texts(language: str = 'ru'):
    js = asyncj.AsyncJson("texts.json")
    texts = await js.read()
    return texts.get(language, texts['ru'])


async def load_settings():
    js = asyncj.AsyncJson("./config/settings.json")
    return await js.read()


async def write_settings(**kwargs):
    js = asyncj.AsyncJson("texts.json")
    return await js.write(kwargs)
