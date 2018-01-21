# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
import base64
from settings import USER_AGENTS
from settings import PROXIES

class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent",useragent)


class RandomProxy(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        print '---------------------'
        print proxy
        if proxy['user_passwd'] is None:
            # 如果没有代理账户验证
            request.meta['proxy'] = "http://" + proxy['ip_port']
        else:
            base64_userpasswd = base64.b64encode(proxy['user_passwd'])
            # 对账户密码进行base64编码转换
            request.meta['proxy'] = "http://" + proxy['ip_port']
            # 对应到代理服务器的信令格式里
            request.headers['Proxy-Authorization'] = 'Basic '+ base64_userpasswd
            '''
    为什么HTTP代理要使用base64编码：

    HTTP代理的原理很简单，就是通过HTTP协议与代理服务器建立连接，
    协议信令中包含要连接到的远程主机的IP和端口号，如果有需要身份验证的话还需要加上授权信息，
    服务器收到信令后首先进行身份验证，通过后便与远程主机建立连接，连接成功之后会返回给客户端200，
    表示验证通过，就这么简单，下面是具体的信令格式：

    CONNECT 59.64.128.198:21 HTTP/1.1
    Host: 59.64.128.198:21
    Proxy-Authorization: Basic bGV2I1TU5OTIz
    User-Agent: OpenFetion

    其中Proxy-Authorization是身份验证信息，
    Basic后面的字符串是用户名和密码组合后进行base64编码的结果，
    也就是对username:password进行base64编码。

    HTTP/1.0 200 Connection established

    OK，客户端收到收面的信令后表示成功建立连接，
    接下来要发送给远程主机的数据就可以发送给代理服务器了，
    代理服务器建立连接后会在根据IP地址和端口号对应的连接放入缓存，
    收到信令后再根据IP地址和端口号从缓存中找到对应的连接，将数据通过该连接转发出去。

            '''
