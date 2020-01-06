#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on Jun 28, 2018
@author: Simon
'''
from ws4py.client.threadedclient import WebSocketClient
#from ws4py.client.
from ws4py.client.threadedclient import WebSocketClient
import time

class EchoClient(WebSocketClient):
    def opened(self):
        print("Hey, we are in opened() of class EchoClient")
        def data_provider():
            for i in range(0, 200, 25):
                yield "#" * i

        # self.send(data_provider())
        print("Start to send command!")
        print("we send No1 cmd!")
        self.send(u"?LOGIN_PAGE-admin")
        time.sleep(5)
        print("we send No2 cmd!")
        self.send(u"?VIDOUT_SCALE")
        time.sleep(5)
        print("we send No3 cmd!")
        self.send(u"?VIDOUT_ASPECT_RATIO")

        # for i in range(0, 200, 25):
        #     self.send("*" * i)

    def closed(self, code, reason):
        print(("Closed down", code, reason))

    def received_message(self, m):
        print("Hey, we are in received_message() of class EchoClient！")
        print("#%d" % len(m))
        print(m)
        if len(m) == 175:
            self.close(reason='bye bye')


try:
    # ws = EchoClient('ws://localhost:9000/ws', protocols=['http-only', 'chat'],
    # headers=[('X-Test', 'hello there')])
    ws = EchoClient('wss://192.168.1.112/websocket/', protocols=['http-only', 'chat'],
                    headers=[('X-Test', 'hello there')])
    ws.connect()
    ws.run_forever()
except KeyboardInterrupt:
    ws.close()








# class DummyClient(WebSocketClient):
#     def opened(self):
#         def data_provider():
#             for i in range(1, 200, 50):
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
#         print("recieved message!")
#         if len(m) == 175:
#             self.close(reason='Bye bye')
#
# if __name__ == '__main__':
#     try:
#         ws = DummyClient('wss://192.168.1.112/websocket/', protocols=['http-only', 'chat'])
#         ws.connect()
#         ws.opened()
#         res=ws.received_message(u"?LOGIN_PAGE-admin")
#         #res = ws.run_forever()
#         # data = r'{"data":[{"login":{"ni_username":{"value":"administrator"},"ni_password":{"value":"password"}}}],"action":"exe","rsp":[]}'
#         # ws.send(data)
#         # ws.close()
#         # ws = DummyClient('wss://192.168.1.218/web/master?sessionid=/', protocols=['http-only', 'chat'])
#         # ws.connect()
#         # wslogin = DummyClient('wss://192.168.1.218/web/login?sessionid=/', protocols=['http-only', 'chat'])
#         # wslogin.connect()
#         #ws.send(u"?LOGIN_PAGE-admin")
#         #ws.send(u"VIDOUT_SCALE-AUTO")
#         #ws.send(u"VIDOUT_ASPECT_RATIO-STRETCH")
#         #ws.send(u"?VIDOUT_SCALE")
#         print("Simon, %s" % res)
#     except KeyboardInterrupt:
#         ws.close()
# # import json
# # from ws4py.client.threadedclient import WebSocketClient
# #
# #
# # class CG_Client(WebSocketClient):
# #
# #     def opened(self):
# #         req = '{"event":"subscribe", "channel":"eth_usdt.deep"}'
# #         self.send(req)
# #
# #     def closed(self, code, reason=None):
# #         print("Closed down:", code, reason)
# #
# #     def received_message(self, resp):
# #         resp = json.loads(str(resp))
# #         data = resp['data']
# #         if type(data) is dict:
# #             ask = data['asks'][0]
# #             print('Ask:', ask)
# #             bid = data['bids'][0]
# #             print('Bid:', bid)
# #
# #
# # if __name__ == '__main__':
# #     ws = None
# #     try:
# #         print("Haha!")
# #         ws = CG_Client('wss://192.168.1.177/websocket')
# #         #ws = CG_Client('wss://i.cg.net/wi/ws')
# #         ws.connect()
# #         ws.run_forever()
# #     except KeyboardInterrupt:
# #         ws.close()
#
# # from websocket import create_connection
# # import ssl
# # import urllib.request, urllib.response
# # import websocket
# # import socket
# #
# # # class client_ssl:
# # #     def send_hello(self,):
# # #         # 生成SSL上下文
# # #         context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
# # #         # 加载信任根证书
# # #         context.load_verify_locations('C:\\Program Files\\apache-jmeter-5.1.1\\bin\\ApacheJMeterTemporaryRootCA.crt')
# # #
# # #         # 与服务端建立socket连接
# # #         with socket.create_connection(('192.168.1.177', 443)) as sock:
# # #             # 将socket打包成SSL socket
# # #             # 一定要注意的是这里的server_hostname不是指服务端IP，而是指服务端证书中设置的CN，我这里正好设置成127.0.1而已
# # #             with context.wrap_socket(sock, server_hostname='192.168.1.177/websocket') as ssock:
# # #                 # 向服务端发送信息
# # #                 msg = "do i connect with server ?".encode("utf-8")
# # #                 ssock.send(msg)
# # #                 # 接收服务端返回的信息
# # #                 msg = ssock.recv(1024).decode("utf-8")
# # #                 print(f"receive msg from server : {msg}")
# # #                 ssock.close()
# # #
# # # if __name__ == "__main__":
# # #     client = client_ssl()
# # #     client.send_hello()
# #
# # def on_message(ws, message):  # 服务器有数据更新时，主动推送过来的数据
# #     print(message)
# #
# #
# # def on_error(ws, error):  # 程序报错时，就会触发on_error事件
# #     print(error)
# #
# #
# # def on_close(ws):
# #     print("Connection closed ……")
# #
# #
# # def on_open(ws):  # 连接到服务器之后就会触发on_open事件，这里用于send数据
# #     print("In Open...")
# #     req = 'hello world'
# #     print(req)
# #     #ws.send(req)
# #
# #
# # if __name__ == "__main__":
# #     ssl._create_default_https_context = ssl._create_unverified_context
# #     #ssl._create_default_https_context = ssl._create_unverified_context
# #     cont = ssl._create_unverified_context()
# #     urls='https://192.168.1.177'
# #     req = urllib.request.Request(urls)
# #     response = urllib.request.urlopen(url=req, context=cont)
# #     print((response.read().decode('utf-8')))
# #     websocket.enableTrace(True)
# #
# #     # #ws = websocket.WebSocketApp("wss://i.cg.net/wi/ws",on_message=on_message,on_error=on_error,on_close=on_close)
# #     # ws = websocket.WebSocketApp("wss://192.168.1.112/websocket/",on_message=on_message,on_error=on_error,on_close=on_close)
# #     # #on_open(ws)
# #     # #ws.send("Hello World!")
# #     # #ws.run_forever(ping_timeout=30)
# #     #ws = create_connection("wss://192.168.1.112/websocket/",sslopt={"cer_reqs":ssl.CERT_NONE})
# #     #ws = websocket.WebSocket(sslopt={"cer_reqs":ssl.CERT_NONE})
# #     #
# #     # ws = websocket.WebSocket(sslopt={"check_hostname":False,"cer_reqs":ssl.CERT_NONE})
# #     # ws.connect("wss://192.168.1.177/websocket/")
# #     # print("Hello world")
# #     # ws.send("Hello,World")
# #     # print("Recieving...")
# #     # result=ws.recv()
# #
# # # hostname = '192.168.1.177'
# # # webhostname = hostname+'/websocket/'
# # # #context = ssl.create_default_context()
# # # context = ssl._create_unverified_context()
# # #
# # # with socket.create_connection((hostname, 443)) as sock:
# # #     with context.wrap_socket(sock, server_hostname=webhostname) as ssock:
# # #         print(ssock.version())
# # #         print(type(ssock))
# # #         ssock.send(bytes("?LOGIN_PAGE-admin".encode("utf8")))
# # #         result = ssock.recv()
# # #         print(bytes.decode(result))
# #
# #     ws = create_connection("wss://192.168.1.177/websocket/",443, sslopt={"cert_reqs": ssl.CERT_NONE})
# #     ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})