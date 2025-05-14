"""
Root response service class.
"""

import asyncio

from loguru import logger

from src.schemas.root_response import RootResponse
from src.utils.random_util import get_random_value


class RootResponseService:
    """
    Root response service class.
    """

    @staticmethod
    async def get_root_response() -> RootResponse:
        """
        Get root response.

        :returns: root response.
        """
        seconds = get_random_value(7)
        logger.debug(f"Sleeping for {seconds} seconds before answering request.")
        await asyncio.sleep(seconds)
        return RootResponse(message="Hello World message from the back-end!")
