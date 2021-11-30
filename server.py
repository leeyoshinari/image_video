#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import os
import asyncio
import jinja2
from aiohttp import web
import aiohttp_jinja2

from common.config import getServer
from common.mysql import get_answer


async def home(request):
    return aiohttp_jinja2.render_template('home.html', request, context={})


async def comment(request):
    return aiohttp_jinja2.render_template('home.html', request, context={})


async def answer(request):
    answer_id = request.query.get('aId')
    results = get_answer(answer_id)
    return aiohttp_jinja2.render_template('home.html', request, context={'datas': results})


async def finder(request):
    return aiohttp_jinja2.render_template('home.html', request, context={})


async def images(request):
    return aiohttp_jinja2.render_template('home.html', request, context={})

async def main():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader = jinja2.FileSystemLoader('templates'))
    app.router.add_static(f'{getServer("serverContext")}/static/',
                          path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
                          append_version=True)
    app.router.add_route('GET', '', home)
    app.router.add_route('GET', '/common', comment)
    app.router.add_route('GET', '/answer', answer)
    app.router.add_route('GET', '/find', finder)
    app.router.add_route('GET', '/images', images)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, getServer('ip'), getServer('port'))
    await site.start()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
