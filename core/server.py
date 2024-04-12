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

import starlette_plus
from starlette.middleware import Middleware

from .config import config
from .database import Database


class Application(starlette_plus.Application):
    def __init__(self, *, database: Database) -> None:
        self.database: Database = database

        redis_rate: starlette_plus.Redis = starlette_plus.Redis(url="redis://localhost:6379/10")
        redis_sess: starlette_plus.Redis = starlette_plus.Redis(url="redis://localhost:6379/11")

        secret: str = config["SERVER"]["secret"]

        ratelimiter: Middleware = Middleware(starlette_plus.middleware.RatelimitMiddleware, redis=redis_rate)
        sessions: Middleware = Middleware(starlette_plus.middleware.SessionMiddleware, redis=redis_sess, secret=secret)

        middleware: list[Middleware] = [ratelimiter, sessions]
        super().__init__(middleware=middleware)

    @starlette_plus.route("/test")
    async def test_route(self, request: starlette_plus.Request) -> starlette_plus.Response:
        return starlette_plus.Response("Hello, World!")
