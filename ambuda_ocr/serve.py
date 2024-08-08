import json
from collections.abc import Callable
import re
from typing import Any

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
import pdf_image_extract

async def homepage(request: Request):
    return JSONResponse({'hello': 'world'})


async def done(request: Request):
    qp = request.query_params['prefix']
    return PlainTextResponse(f"done  {qp}")


async def dispatch(request: Request, fn: Callable[[Any], Any]):
    print(request.method)
    print(request.url.path)
    o = json.loads(await request.body())
    print(o)
    r = await fn(o)
    print(r)
    return JSONResponse(r)


async def pdf(request: Request):
    return await dispatch(request, pdf_image_extract.run)


app = Starlette(debug=True, routes=[
    Route('/', homepage),
    Route('/pdf', pdf, methods=['POST']),
    Route('/done', done, methods=['GET']),
])
