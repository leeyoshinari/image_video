#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import os
import asyncio
import jinja2
from aiohttp import web
import aiohttp_jinja2

from common.config import getServer
from common.deal_ip import IPQueue
from common.mysql import get_answer, get_comment, get_key_word, get_forum, get_similarity
from common.logger import logger


FIFO = IPQueue()


async def home(request):
    host = request.headers.get('X-Real-IP')
    FIFO.put_queue(host)
    FIFO.put_queue('home')
    logger.info(f'{host} - home')
    return aiohttp_jinja2.render_template('template.html', request, context={'context': getServer("serverContext"), 'setting': ''})


async def comment(request):
    host = request.headers.get('X-Real-IP')
    user_id = request.query.get('userId')
    user_id = user_id.replace('%', '').replace('+', '')
    types = request.query.get('type')
    page = request.query.get('page')
    auth = request.query.get('auth')
    page = int(page) if page else 1
    if auth != getServer('auth'):
        page = page if page < 3 else 2
    setting = f'{types},{user_id},{page}'
    FIFO.put_queue(host)
    FIFO.put_queue('comment')
    logger.info(f'{host} - comment - {setting}')
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_comment(user_id, (page - 1) * 15)
    if auth != getServer('auth'):
        total_page = total_page if total_page < 31 else 30
    if results:
        return aiohttp_jinja2.render_template('comment.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def answer(request):
    host = request.headers.get('X-Real-IP')
    answer_id = request.query.get('aId')
    answer_id = answer_id.replace('%', '').replace('+', '')
    types = request.query.get('type')
    page = request.query.get('page')
    auth = request.query.get('auth')
    page = int(page) if page else 1
    if auth != getServer('auth'):
        page = page if page < 3 else 2
    setting = f'{types},{answer_id},{page}'
    FIFO.put_queue(host)
    FIFO.put_queue('answer')
    logger.info(f'{host} - answer - {setting}')
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_answer(answer_id, (page - 1) * 15)
    if auth != getServer('auth'):
        total_page = total_page if total_page < 31 else 30
    if results:
        return aiohttp_jinja2.render_template('answer.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def finder(request):
    host = request.headers.get('X-Real-IP')
    venture = request.query.get('venture')
    key_word = request.query.get('keyWord')
    key_word = key_word.replace('%', '').replace('+', '')
    types = request.query.get('type')
    page = request.query.get('page')
    auth = request.query.get('auth')
    page = int(page) if page else 1
    if auth != getServer('auth'):
        page = page if page < 3 else 2
    setting = f'{types},{venture},{key_word},{page}'
    FIFO.put_queue(host)
    FIFO.put_queue('finder')
    logger.info(f'{host} - finder - {setting}')
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_key_word(venture, key_word, (page - 1) * 15)
    if auth != getServer('auth'):
        total_page = total_page if total_page < 31 else 30
    if results:
        return aiohttp_jinja2.render_template('answer.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def similarity(request):
    host = request.headers.get('X-Real-IP')
    answer_id = request.query.get('aId')
    answer_id = answer_id.replace('%', '').replace('+', '')
    types = request.query.get('type')
    page = request.query.get('page')
    auth = request.query.get('auth')
    init_status = request.query.get('init')
    page = int(page) if page else 1
    if auth != getServer('auth'):
        page = page if page < 3 else 2
    setting = f'{types},{answer_id},{page}'
    FIFO.put_queue(host)
    FIFO.put_queue('similarity')
    logger.info(f'{host} - similarity - {setting}')
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_similarity(answer_id, (page - 1) * 15, init_status)
    if auth != getServer('auth'):
        total_page = total_page if total_page < 31 else 30
    if results:
        return aiohttp_jinja2.render_template('similarity.html', request,
                                              context={'context': getServer("serverContext"), 'datas': results,
                                                       'setting': setting, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request,
                                              context={'context': getServer("serverContext"), 'setting': setting})


async def images(request):
    host = request.headers.get('X-Real-IP')
    return aiohttp_jinja2.render_template('template.html', request, context={'context': getServer("serverContext"), })


async def forum(request):
    host = request.headers.get('X-Real-IP')
    page = request.query.get('page')
    search_type = request.query.get('searchType')
    order_type = request.query.get('orderType')
    page = int(page) if page else 1
    search_type = search_type if search_type else 'time'
    order_type = order_type if order_type else 'desc'
    FIFO.put_queue(host)
    FIFO.put_queue('forum')
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext")})
    results, total_page = get_forum((page - 1) * 10, search_type, order_type)
    if results:
        return aiohttp_jinja2.render_template('forum.html', request,
                                              context={'context': getServer("serverContext"), 'datas': results, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext")})


async def course(request):
    host = request.headers.get('X-Real-IP')
    FIFO.put_queue(host)
    FIFO.put_queue('course')
    return aiohttp_jinja2.render_template('course.html', request, context={'context': getServer("serverContext"), })


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
    app.router.add_route('GET', f'{getServer("serverContext")}/forum', forum)
    app.router.add_route('GET', f'{getServer("serverContext")}/similarity', similarity)
    app.router.add_route('GET', f'{getServer("serverContext")}/course', course)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, getServer('ip'), getServer('port'))
    await site.start()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
