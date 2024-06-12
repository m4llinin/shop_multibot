from aiogram.utils.token import TokenValidationError


async def is_bot_token(token: str):
    try:
        if not isinstance(token, str):
            raise TokenValidationError(
                f"Token is invalid! It must be 'str' type instead of {type(token)} type."
            )

        if any(x.isspace() for x in token):
            message = "Token is invalid! It can't contains spaces."
            raise TokenValidationError(message)

        left, sep, right = token.partition(":")
        if (not sep) or (not left.isdigit()) or (not right):
            raise TokenValidationError("Token is invalid!")
    except TokenValidationError:
        return False
    return True
