# # from websocket import create_connection
# # import ssl
# # #ws = create_connection("ws://echo.websocket.org/",sslopt=None)
# # ws = create_connection("wss://192.168.1.112/websocket/",sslopt={"cert_reqs":ssl.CERT_NONE,"check_hostname":False,"ssl_version":ssl.PROTOCOL_SSLv23})
# # print("Sending 'Hello, World'...")
# # # ws.send(bytes("Hello, World!!!", encoding='utf8'))
# # # result = ws.recv()
# # # print("Received '%s'" % result)
# # ws.send("?LOGIN_PAGE-admin")
# # ws1 = create_connection("wss://192.168.1.112/websocket/",sslopt={"cert_reqs":ssl.CERT_NONE,"check_hostname":False,"ssl_version":ssl.PROTOCOL_SSLv23})
# # ws1.send(bytes("VIDOUT_SCALE-MANUAL", encoding='utf8'))
# # result2 = ws1.recv()
# # print("Received2 '%s'" % result2)
# # ws.close()
# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# '''
# Created on Jun 28, 2018
# @author: Simon
# '''
# from ws4py.client.threadedclient import WebSocketClient
# #from ws4py.client.
#
# class DummyClient(WebSocketClient):
#     def opened(self):
#         def data_provider():
#             for i in range(1, 200, 25):
#                 yield "#" * i
#
#         self.send(data_provider())
#
#         for i in range(0, 200, 25):
#             print(i)
#             self.send("*" * i)
#
#     def closed(self, code, reason=None):
#         print("Closed down", code, reason)
#
#     def received_message(self, m):
#         print(m)
#         if len(m) == 175:
#             self.close(reason='Bye bye')
#
# if __name__ == '__main__':
#     try:
#         ws = DummyClient('wss://192.168.1.112/websocket/', protocols=['http-only', 'chat'])
#         ws.connect()
#         #ws.run_forever()
#         # data = r'{"data":[{"login":{"ni_username":{"value":"administrator"},"ni_password":{"value":"password"}}}],"action":"exe","rsp":[]}'
#         # ws.send(data)
#         # ws.close()
#         # ws = DummyClient('wss://192.168.1.218/web/master?sessionid=/', protocols=['http-only', 'chat'])
#         # ws.connect()
#         # wslogin = DummyClient('wss://192.168.1.218/web/login?sessionid=/', protocols=['http-only', 'chat'])
#         # wslogin.connect()
#         #ws.send(u"?LOGIN_PAGE-admin")
#         ws.send(u"VIDOUT_SCALE-AUTO")
#         #ws.send(u"VIDOUT_ASPECT_RATIO-STRETCH")
#     except KeyboardInterrupt:
#         ws.close()

import asyncio
import logging
from datetime import datetime
from aiowebsocket.converses import AioWebSocket


async def startup(uri):
    async with AioWebSocket(uri) as aws:
        converse = aws.manipulator
        message = b'AioWebSocket - Async WebSocket Client'
        while True:
            await converse.send(message)
            print('{time}-Client send: {message}'
                  .format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message=message))
            mes = await converse.receive()
            print('{time}-Client receive: {rec}'
                  .format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rec=mes))


if __name__ == '__main__':
    remote = 'wss://192.168.1.112/websocket/'
    #remote = 'wss://echo.websocket.org'
    try:
        asyncio.get_event_loop().run_until_complete(startup(remote))
    except KeyboardInterrupt as exc:
        logging.info('Quit.')