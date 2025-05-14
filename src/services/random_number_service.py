"""
Random number service class.
"""

import asyncio

from loguru import logger

from src.schemas.random_number import RandomResponse
from src.utils.random_util import get_random_value


class RandomResponseService:
    """
    Random number service class.
    """

    @staticmethod
    async def get_random_number() -> RandomResponse:
        """
        Get random number.

        :returns: random number.
        """
        seconds = get_random_value(5)
        logger.debug(f"Sleeping for {seconds} seconds before answering request.")
        await asyncio.sleep(seconds)
        return RandomResponse(message=round(seconds, 2))
