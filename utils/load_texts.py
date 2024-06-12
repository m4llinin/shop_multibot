import asyncj


async def load_texts(language: str = 'ru'):
    js = asyncj.AsyncJson("texts.json")
    texts = await js.read()
    return texts.get(language, texts['ru'])
