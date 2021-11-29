#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import os
import asyncio
import jinja2
from aiohttp import web
import aiohttp_jinja2

from common.config import getServer


async def home(request):
    return aiohttp_jinja2.render_template('home.html', request, context={})


async def home(request):
    return aiohttp_jinja2.render_template('home.html', request, context={})


async def main():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader = jinja2.FileSystemLoader('templates'))
    app.router.add_static(f'{getServer("serverContext")}/static/',
                          path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
                          append_version=True)
    app.router.add_route('GET', '', home)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, getServer('ip'), getServer('port'))
    await site.start()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
