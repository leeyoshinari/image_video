#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import os
import time
import json
import asyncio
import traceback
import redis
import jinja2
from aiohttp import web
import aiohttp_jinja2

from common.config import getServer, user_name, DateEncoder
from common.deal_ip import IPQueue
from common.mysql import *
from common.logger import logger


FIFO = IPQueue()
r = redis.Redis(host=getServer('redis_host'), port=getServer('redis_port'), password=getServer('redis_pwd'))
freq = int(getServer('r_freq'))


async def home(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    FIFO.put_queue((host, current_time))
    FIFO.put_queue(('home', current_time))
    FIFO.put_queue((host, user_agent, current_time))
    logger.info(f'{host} - home')
    return aiohttp_jinja2.render_template('template.html', request, context={'context': getServer("serverContext"), 'setting': ''})


async def comment(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    f = request.query.get('f')
    if f == getServer('r_auth'):
        r.delete('comment')
    if r.get('comment'):
        return aiohttp_jinja2.render_template('520.html', request, context={'context': getServer("serverContext")})
    user_id = request.query.get('userId')
    user_id = user_id.replace('%', '').replace('+', '')
    types = request.query.get('type')
    page = request.query.get('page')
    auth = request.query.get('auth')
    page = int(page) if page else 1
    if auth != getServer('p_auth'):
        page = page if page < 3 else 2
    setting = f'{types},{user_id},{page}'
    FIFO.put_queue((host, current_time))
    FIFO.put_queue(('comment', current_time))
    FIFO.put_queue((host, user_agent, current_time))
    logger.info(f'{host} - comment - {setting}')
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_comment(user_id, (page - 1) * 15)
    r.set('comment', 1, ex=freq)
    if auth != getServer('p_auth'):
        total_page = total_page if total_page < 31 else 30
    if results:
        return aiohttp_jinja2.render_template('comment.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def answer(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    f = request.query.get('f')
    if f == getServer('r_auth'):
        r.delete('answer')
    if r.get('answer'):
        return aiohttp_jinja2.render_template('520.html', request, context={'context': getServer("serverContext")})
    answer_id = request.query.get('aId')
    answer_id = answer_id.replace('%', '').replace('+', '')
    types = request.query.get('type')
    page = request.query.get('page')
    auth = request.query.get('auth')
    page = int(page) if page else 1
    if auth != getServer('p_auth'):
        page = page if page < 3 else 2
    setting = f'{types},{answer_id},{page}'
    FIFO.put_queue((host, current_time))
    FIFO.put_queue(('answer', current_time))
    FIFO.put_queue((host, user_agent, current_time))
    logger.info(f'{host} - answer - {setting}')
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_answer(answer_id, (page - 1) * 15)
    r.set('answer', 1, ex=freq)
    if auth != getServer('p_auth'):
        total_page = total_page if total_page < 31 else 30
    if results:
        return aiohttp_jinja2.render_template('answer.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def finder(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    f = request.query.get('f')
    if f == getServer('r_auth'):
        r.delete('finder')
    if r.get('finder'):
        return aiohttp_jinja2.render_template('520.html', request, context={'context': getServer("serverContext")})
    venture = request.query.get('venture')
    key_word = request.query.get('keyWord')
    key_word = key_word.replace('%', '').replace('+', '')
    types = request.query.get('type')
    page = request.query.get('page')
    auth = request.query.get('auth')
    page = int(page) if page else 1
    if auth != getServer('p_auth'):
        page = page if page < 3 else 2
    setting = f'{types},{venture},{key_word},{page}'
    FIFO.put_queue((host, current_time))
    FIFO.put_queue(('finder', current_time))
    FIFO.put_queue((host, user_agent, current_time))
    logger.info(f'{host} - finder - {setting}')
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_key_word(venture, key_word, (page - 1) * 15)
    r.set('finder', 1, ex=freq)
    if auth != getServer('p_auth'):
        total_page = total_page if total_page < 31 else 30
    if results:
        return aiohttp_jinja2.render_template('answer.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def similarity(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    f = request.query.get('f')
    if f == getServer('r_auth'):
        r.delete('similarity')
    if r.get('similarity'):
        return aiohttp_jinja2.render_template('520.html', request, context={'context': getServer("serverContext")})
    answer_id = request.query.get('aId')
    answer_id = answer_id.replace('%', '').replace('+', '')
    types = request.query.get('type')
    page = request.query.get('page')
    auth = request.query.get('auth')
    init_status = request.query.get('init')
    page = int(page) if page else 1
    if auth != getServer('p_auth'):
        page = page if page < 3 else 2
    setting = f'{types},{answer_id},{page}'
    FIFO.put_queue((host, current_time))
    FIFO.put_queue(('similarity', current_time))
    FIFO.put_queue((host, user_agent, current_time))
    logger.info(f'{host} - similarity - {setting}')
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results, total_page = get_similarity(answer_id, (page - 1) * 15, init_status)
    r.set('similarity', 1, ex=freq)
    if auth != getServer('p_auth'):
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
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    f = request.query.get('f')
    if f == getServer('r_auth'):
        r.delete('forum')
    if r.get('forum'):
        return aiohttp_jinja2.render_template('520.html', request, context={'context': getServer("serverContext")})
    page = request.query.get('page')
    search_type = request.query.get('searchType')
    order_type = request.query.get('orderType')
    page = int(page) if page else 1
    search_type = search_type if search_type else 'time'
    order_type = order_type if order_type else 'desc'
    setting = f'{search_type},{order_type},{page}'
    FIFO.put_queue((host, current_time))
    FIFO.put_queue(('forum', current_time))
    FIFO.put_queue((host, user_agent, current_time))
    if page < 1:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext")})
    results, total_page = get_forum((page - 1) * 10, search_type, order_type)
    r.set('forum', 1, ex=freq)
    if results:
        return aiohttp_jinja2.render_template('forum.html', request, context={'context': getServer("serverContext"),
                                              'setting': setting, 'datas': results, 'total': total_page, 'page': page})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext")})


async def course(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    FIFO.put_queue((host, current_time))
    FIFO.put_queue(('course', current_time))
    FIFO.put_queue((host, user_agent, current_time))
    return aiohttp_jinja2.render_template('course.html', request, context={'context': getServer("serverContext")})


async def addComment(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if r.get('addComment'):
        return web.json_response({'code': 0, 'msg': "当前系统繁忙，请稍后再试 ~ ", 'data': None})
    data = json.loads(await request.text())
    user_id = user_name(host) if host else '2020520'
    parent_id = data['id'] if data['id'] else ''
    comment_data = (parent_id, user_id, data['content'], current_time)
    FIFO.put_queue((host, current_time))
    FIFO.put_queue(('addComment', current_time))
    FIFO.put_queue((host, user_agent, current_time))
    try:
        add_comment(comment_data)
        r.set('addComment', 1, ex=freq)
        return web.json_response({'code': 1, 'msg': "Comment Successfully ! ", 'data': None})
    except Exception as err:
        logger.error(traceback.format_exc())
        return web.json_response({'code': 0, 'msg': '系统异常，请稍后重试！', 'data': None})


async def addConnect(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if r.get('addConnect'):
        return web.json_response({'code': 0, 'msg': "当前系统繁忙，请稍后再试 ~ ", 'data': None})
    data = json.loads(await request.text())
    host = host if host else ''
    contact_data = (host, data['tel'], data['content'], current_time)
    FIFO.put_queue((host, current_time))
    FIFO.put_queue(('addConnect', current_time))
    FIFO.put_queue((host, user_agent, current_time))
    try:
        add_connect(contact_data)
        r.set('addConnect', 1, ex=freq)
        return web.json_response({'code': 1, 'msg': "Comment Successfully ! ", 'data': None})
    except Exception as err:
        logger.error(traceback.format_exc())
        return web.json_response({'code': 0, 'msg': '系统异常，请稍后重试！', 'data': None})


async def get_contacts(request):
    results = get_contact()
    if results:
        return aiohttp_jinja2.render_template('message.html', request, context={'context': getServer("serverContext"),
                                                                              'datas': results})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext")})


async def getCommentById(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if r.get('getCommentById'):
        return web.json_response({'code': 0, 'msg': "当前系统繁忙，请稍后再试 ~ ", 'data': None})
    comment_id = request.query.get('Id')
    if not comment_id:
        return web.json_response({'code': 0, 'msg': "未查询到内容，请稍后再试 ~ ", 'data': None})
    FIFO.put_queue((host, current_time))
    FIFO.put_queue(('getCommentById', current_time))
    FIFO.put_queue((host, user_agent, current_time))
    try:
        result = get_comment_by_id(comment_id)
        r.set('getCommentById', 1, ex=freq)
        return web.json_response({'code': 1, 'msg': "Successfully ! ", 'data': json.loads(json.dumps(result, cls=DateEncoder))})
    except:
        logger.error(traceback.format_exc())
        return web.json_response({'code': 0, 'msg': "系统异常，请稍后重试！", 'data': None})


async def dashboard(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    # FIFO.put_queue((host, current_time))
    # FIFO.put_queue(('dashboard', current_time))
    # FIFO.put_queue((host, user_agent, current_time))
    try:
        result = get_pie()
        return aiohttp_jinja2.render_template('dashboard.html', request, context={'context': getServer("serverContext"),
                                                                                  'datas': json.dumps(result)})
    except:
        logger.error(traceback.format_exc())
        return web.json_response({'code': 0, 'msg': "系统异常，请稍后重试！", 'data': None})


async def back_answer(request):
    auth = request.query.get('auth')
    answer_id = request.query.get('aId')
    answer_id = answer_id.replace('%', '').replace('+', '')
    setting = f'0,{answer_id}'
    if auth != getServer('p_auth'):
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results = get_d_answer(answer_id)
    if results:
        return aiohttp_jinja2.render_template('answer.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': 1, 'page': 1})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def back_comment(request):
    auth = request.query.get('auth')
    answer_id = request.query.get('aId')
    answer_id = answer_id.replace('%', '').replace('+', '')
    setting = f'0,{answer_id}'
    if auth != getServer('p_auth'):
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})
    results = get_d_comment(answer_id)
    if results:
        return aiohttp_jinja2.render_template('bd_comment.html', request, context={'context': getServer("serverContext"), 'datas': results, 'setting': setting, 'total': 1, 'page': 1})
    else:
        return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext"), 'setting': setting})


async def BdCommentById(request):
    comment_id = request.query.get('Id')
    if not comment_id:
        return web.json_response({'code': 0, 'msg': "未查询到内容，请稍后再试 ~ ", 'data': None})
    try:
        result = get_comment_by_id(comment_id)
        return web.json_response({'code': 1, 'msg': "Successfully ! ", 'data': json.loads(json.dumps(result, cls=DateEncoder))})
    except:
        logger.error(traceback.format_exc())
        return web.json_response({'code': 0, 'msg': "系统异常，请稍后重试！", 'data': None})


async def test(request):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    FIFO.put_queue(('None', current_time))
    return aiohttp_jinja2.render_template('404.html', request, context={'context': getServer("serverContext")})


async def main():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader = jinja2.FileSystemLoader('templates'))
    app.router.add_static(f'{getServer("serverContext")}/static/',
                          path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
                          append_version=True)
    app.router.add_route('GET', f'{getServer("serverContext")}/testtest', test)
    app.router.add_route('GET', f'{getServer("serverContext")}', course)
    app.router.add_route('GET', f'{getServer("serverContext")}/comment', comment)
    app.router.add_route('GET', f'{getServer("serverContext")}/answer', answer)
    app.router.add_route('GET', f'{getServer("serverContext")}/find', finder)
    app.router.add_route('GET', f'{getServer("serverContext")}/images', images)
    app.router.add_route('GET', f'{getServer("serverContext")}/forum', forum)
    app.router.add_route('GET', f'{getServer("serverContext")}/similarity', similarity)
    app.router.add_route('GET', f'{getServer("serverContext")}/course', course)
    app.router.add_route('POST', f'{getServer("serverContext")}/addComment', addComment)
    app.router.add_route('POST', f'{getServer("serverContext")}/addConnect', addConnect)
    app.router.add_route('GET', f'{getServer("serverContext")}/contact', get_contacts)
    app.router.add_route('GET', f'{getServer("serverContext")}/getCommentById', getCommentById)
    app.router.add_route('GET', f'{getServer("serverContext")}/dashboard', dashboard)
    app.router.add_route('GET', f'{getServer("serverContext")}/BDAnswer', back_answer)
    app.router.add_route('GET', f'{getServer("serverContext")}/BDComment', back_comment)
    app.router.add_route('GET', f'{getServer("serverContext")}/BDCommentById', BdCommentById)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, getServer('ip'), getServer('port'))
    await site.start()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
