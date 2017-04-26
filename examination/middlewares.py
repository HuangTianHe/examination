import base64
# -*- coding:utf-8 -*-
# 代理服务器
proxyServer = "http://proxy.abuyun.com:9010"

# 代理隧道验证信息
proxyUser = "HCS05S2JV395370D"
proxyPass = "955AD23A8F2EEA0B"

proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass)

class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        #request.meta['proxy'] = "http://YOUR_PROXY_IP:PORT"
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth   
