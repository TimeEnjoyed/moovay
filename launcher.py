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

import starlette_plus
import uvicorn

import core


starlette_plus.setup_logging(level=20)


async def main() -> None:
    config = core.config["SERVER"]

    async with core.Database() as db:
        app: core.Application = core.Application(database=db)

        uvconf: uvicorn.Config = uvicorn.Config(app=app, host=config["host"], port=config["port"], access_log=False)
        server: uvicorn.Server = uvicorn.Server(config=uvconf)

        await server.serve()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
