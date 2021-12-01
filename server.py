#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import os
import asyncio
import jinja2
from aiohttp import web
import aiohttp_jinja2

from common.config import getServer
from common.mysql import get_answer, get_comment, get_key_word


async def home(request):
    return aiohttp_jinja2.render_template('template.html', request, context={})


async def comment(request):
    user_id = request.query.get('userId')
    results = get_comment(user_id)
    if results:
        return aiohttp_jinja2.render_template('comment.html', request, context={'datas': results})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={})


async def answer(request):
    answer_id = request.query.get('aId')
    results = get_answer(answer_id)
    if results:
        return aiohttp_jinja2.render_template('answer.html', request, context={'datas': results})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={})


async def finder(request):
    question_id = request.query.get('qId')
    key_word = request.query.get('keyWord')
    results = get_key_word(question_id, key_word)
    if results:
        return aiohttp_jinja2.render_template('answer.html', request, context={'datas': results})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={})


async def images(request):
    return aiohttp_jinja2.render_template('home.html', request, context={})

async def main():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader = jinja2.FileSystemLoader('templates'))
    app.router.add_static(f'{getServer("serverContext")}/static/',
                          path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
                          append_version=True)
    app.router.add_route('GET', '', home)
    app.router.add_route('GET', '/comment', comment)
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
