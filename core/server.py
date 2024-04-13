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

import logging

import starlette_plus
from starlette.middleware import Middleware

from .config import config
from .database import Database


logger: logging.Logger = logging.getLogger(__name__)


class Application(starlette_plus.Application):
    def __init__(self, *, database: Database) -> None:
        self.database: Database = database

        secret: str = config["SERVER"]["secret"]
        url_rate: str = config["REDIS"]["url_rate"]
        url_sess: str = config["REDIS"]["url_sess"]

        self.redis_rate: starlette_plus.Redis = starlette_plus.Redis(url=url_rate)
        self.redis_sess: starlette_plus.Redis = starlette_plus.Redis(url=url_sess)

        middleware: list[Middleware] = [
            Middleware(starlette_plus.middleware.RatelimitMiddleware, redis=self.redis_rate),
            Middleware(starlette_plus.middleware.SessionMiddleware, redis=self.redis_sess, secret=secret),
        ]

        super().__init__(on_startup=[self.on_startup], on_shutdown=[self.on_shutdown], middleware=middleware)

    async def on_startup(self) -> None:
        try:
            await self.redis_rate.ping()
            await self.redis_sess.ping()
        except Exception as e:
            raise RuntimeError("Failed to connect to Redis. Shutting down application.") from e

    async def on_shutdown(self) -> None:
        try:
            await self.redis_rate.pool.close()  # type: ignore
            await self.redis_sess.pool.close()  # type: ignore
        except Exception:
            logger.warning("Failed to gracefully close Redis connections. This can most likely be ignored.")

    @starlette_plus.route("/test")
    async def test_route(self, request: starlette_plus.Request) -> starlette_plus.Response:
        return starlette_plus.Response("Hello, World!")
