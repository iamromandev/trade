import asyncio

from loguru import logger


async def send_email(ctx, *, to: str, subject: str = "", body: str = "") -> bool:
    logger.info("Sending email to: {} subject: {}", to, subject)
    await asyncio.sleep(0.1)
    logger.info("Email sent to: {}", to)
    return True
