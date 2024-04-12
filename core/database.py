"""Copyright 2024 https://github.com/TimeEnjoyed

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import asyncio
import logging
from typing import TYPE_CHECKING, Any, Self

import asyncpg

from .config import config


if TYPE_CHECKING:
    _Pool = asyncpg.Pool[asyncpg.Record]
else:
    _Pool = asyncpg.Pool


logger: logging.Logger = logging.getLogger(__name__)


class Database:
    pool: _Pool

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    async def connect(self) -> None:
        try:
            pool: asyncpg.Pool[asyncpg.Record] | None = await asyncpg.create_pool(dsn=config["DATABASE"]["dsn"])
        except Exception as e:
            raise RuntimeError from e

        if not pool:
            raise RuntimeError("Failed to connect to the database... No additional information.")

        with open("schema.sql") as fp:
            await pool.execute(fp.read())

        self.pool = pool
        logger.info("Successfully connected to the database.")

    async def close(self) -> None:
        try:
            await asyncio.wait_for(self.pool.close(), timeout=10)
        except TimeoutError:
            logger.warning("Failed to greacefully close the database connection...")
        else:
            logger.info("Successfully closed the database connection.")
