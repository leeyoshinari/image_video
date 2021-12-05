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
    return aiohttp_jinja2.render_template('template.html', request, context={'context': getServer("serverContext"), 'setting': ''})


async def comment(request):
    user_id = request.query.get('userId')
    types = request.query.get('type')
    page = request.query.get('page')
    page = int(page) if page else 1
    setting = f'{types},{user_id},{page}'
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_comment(user_id, (page-1)*15)
    if results:
        return aiohttp_jinja2.render_template('comment.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def answer(request):
    answer_id = request.query.get('aId')
    types = request.query.get('type')
    page = request.query.get('page')
    page = int(page) if page else 1
    setting = f'{types},{answer_id},{page}'
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_answer(answer_id, (page-1)*15)
    if results:
        return aiohttp_jinja2.render_template('answer.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def finder(request):
    venture = request.query.get('venture')
    key_word = request.query.get('keyWord')
    types = request.query.get('type')
    page = request.query.get('page')
    page = int(page) if page else 1
    setting = f'{types},{venture},{key_word},{page}'
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_key_word(venture, key_word, (page-1)*15)
    if results:
        return aiohttp_jinja2.render_template('answer.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def images(request):
    return aiohttp_jinja2.render_template('template.html', request, context={'context': getServer("serverContext"), })

async def main():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader = jinja2.FileSystemLoader('templates'))
    app.router.add_static(f'{getServer("serverContext")}/static/',
                          path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
                          append_version=True)
    app.router.add_route('GET', f'{getServer("serverContext")}', home)
    app.router.add_route('GET', f'{getServer("serverContext")}/comment', comment)
    app.router.add_route('GET', f'{getServer("serverContext")}/answer', answer)
    app.router.add_route('GET', f'{getServer("serverContext")}/find', finder)
    app.router.add_route('GET', f'{getServer("serverContext")}/images', images)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, getServer('ip'), getServer('port'))
    await site.start()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
