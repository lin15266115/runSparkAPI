# 1.1
# import time
# 以下密钥信息从控制台获取   
answer = ""
sid = ''

class 认证信息:
    """
    你需要注册讯飞星火的账号,购买讯飞星火产品,\n
    并从https://console.xfyun.cn/services/cbm
    获取你的appid, api_secret, api_key并在创建实例时填写进来\n
    
    Parameters:
        APPID (str):控制台中的 appid
        APISecret (str):控制台中的 api_secret
        APIKey (str):控制台中的 api_key
    """
    def __init__(
             self
            ,APPID    : str
            ,APISecret: str
            ,APIKey   : str
        ):
        self.appid      = APPID 
        self.api_secret = APISecret   
        self.api_key    = APIKey


class 星火消息:
    def __init__(
             self
            ,ID: 认证信息
            ,最大字符长度 = 8000
        ):
        """
        星火消息类，用于与讯飞星火API进行交互。
        
        Attributes:
            设定 (dict): 系统角色和内容设定。
            历史 (list): 存储对话历史的消息列表。
            新消息 (str): 待发送的新消息。
            appid (str): 控制台中获取的APPID信息。
            api_secret (str): 控制台中获取的APISecret信息。
            api_key (str): 控制台中获取的APIKey信息。
            最大字符长度 (int): 允许的最大字符长度。
            自动置历史 (bool): 是否自动将用户消息和AI回复添加到历史记录中。
        
        Methods:
            更改ai设定(内容： str): 设置讯飞星火的设定，填入一段文本作为设定内容。
            置最大字符长度(长度： int): 设置允许的最大字符长度。
            置消息历史(role, content: str): 向历史记录中添加一条消息。
            获取回复(使用历史回复=True): 调用内部main函数获取回复，并根据需要更新历史记录。
            置用户消息到历史(text: str): 将用户消息添加到历史记录中。
            置AI回复到历史(text: str): 将AI回复添加到历史记录中。
            取历史消息总长度(): 计算历史记录中所有消息的总字符长度。
            检查消息长度并处理(): 如果消息长度超过最大字符长度，则删除最早的历史记录直到满足条件。
            调用的ai版本(版本： int): 选择使用的讯飞星火API版本。
            自动置历史回复(开关： bool): 设置是否自动将用户消息和AI回复添加到历史记录中。
        """
        self.设定 = {"role": "system", "content": ""}
        self.历史 = []
        self.新消息 = ""
        self.appid = ID.appid     #填写控制台中获取的 APPID 信息
        self.api_secret = ID.api_secret   #填写控制台中获取的 APISecret 信息
        self.api_key = ID.api_key    #填写控制台中获取的 APIKey 信息
        self.调用的ai版本(0)         
        self.最大字符长度 = 最大字符长度
        self.自动置历史 = True
    
    def 更改ai设定(self, 内容:str):
        """设置讯飞星火的设定, 填入一段文本作为设定内容"""
        self.设定 = {"role": "system", "content": 内容 }

    def 置最大字符长度(self,长度:int):
        self.最大字符长度 = 长度

    def 置消息历史(self,role,content:str):
        字典 = {}
        字典["role"] = role
        字典["content"] = content
        self.历史.append(字典)
        

    def 获取回复(
             self
            ,使用历史回复 = True
        ):
        """
        在更新完*self.新消息* 后, 使用这个函数获取AI的回复。如果设定了使用历史回复，那么会将历史消息和当前消息一起发送给AI。然后，根据AI的回复，将其添加到历史记录中（如果开启了自动置历史）。
    
        Parameters:
            self (object): 对象自身。
            使用历史回复 (bool, optional): 让AI回复时参考历史消息，默认为True。
            
        Returns:
            str: AI的回复内容。

        """
        
        总消息 = [self.设定]
        if 使用历史回复 :
            总消息 += self.历史
            self.检查消息长度并处理()

        新消息 = {"role": "user", "content": self.新消息}
        总消息.append(新消息)

        # print(self.消息)
        global answer
        answer = ""
        main( 
             self.appid
            ,self.api_key
            ,self.api_secret
            ,self.Spark_url
            ,self.domain
            ,总消息
        )
        回复 = answer
        if self.自动置历史 :
            self.置用户消息到历史(self.新消息)
            self.置AI回复到历史(回复)
        return 回复

    def 置用户消息到历史(self,text:str): 
        self.置消息历史("user", text)

    def 置AI回复到历史(self,text:str):
        self.置消息历史("assistant", text)

    def 取历史消息总长度(self):
        历史消息总长度 = 0
        for 字典 in self.历史:
            历史消息总长度 += len(字典["content"])
        return 历史消息总长度

    def 检查消息长度并处理(self,):
        while (self.取历史消息总长度() + len(self.新消息) + len(self.设定["content"]) > self.最大字符长度) :
            # 这里其实还能优化()
            if len(self.历史) > 0 :
                del self.历史[0]
            else :
                self.设定["content"] = ""

    def 调用的ai版本(
             self
            ,版本:int
        ):
        """

        调用不同的AI版本。该函数接受一个整数参数，代表要调用的AI版本。
        
        Parameters:
            version (int): 
                可选的数字包括0,1,2,3,4,5，分别对应以下版本：\n
                0 -> Spark Lite\n
                1 -> Spark V2.0\n
                2 -> Spark Pro\n
                3 -> Spark Pro-128K\n
                4 -> Spark Max\n
                5 -> Spark4.0 Ultra\n
        
        Returns:
            None:
            无返回值。但会更改对象的Spark_url和domain属性，以使用相应的AI版本。

        """
        所有版本 = (
            ['wss://spark-api.xf-yun.com/v1.1/chat','general'],       # 0
            ['wss://spark-api.xf-yun.com/v2.1/chat','generalv2'],     # 1
            ['wss://spark-api.xf-yun.com/v3.1/chat','generalv3'],     # 2
            ['wss://spark-api.xf-yun.com/chat/pro-128k','pro-128k'],  # 3
            ['wss://spark-api.xf-yun.com/v3.5/chat','generalv3.5'],   # 4
            ['wss://spark-api.xf-yun.com/v4.0/chat','4.0Ultra']       # 5
        )

        self.Spark_url =所有版本[版本][0]
        self.domain = 所有版本[版本][1]

    def 自动置历史回复(self,开关:bool):
            self.自动置历史 = 开关

# 以下代码来自讯飞星火官方文档
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
import time
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket  # 使用websocket_client
answer = ""
sid = ''

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, Spark_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()

        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.Spark_url + '?' + urlencode(v)
        # print(url)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        return url


# 收到websocket错误的处理
def on_error(ws, error):
    print("### error:", error)


# 收到websocket关闭的处理
def on_close(ws,one,two):
    print("\nwebsocket关闭")


# 收到websocket连接建立的处理
def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, domain= ws.domain,question=ws.question))
    ws.send(data)


# 收到websocket消息的处理
def on_message(ws, message):
    # print(message)
    # print(time.time())
    data = json.loads(message)
    code = data['header']['code']
    if code != 0:
        print(f'请求错误: {code}, {data}')
        ws.close()
    else:
        global sid
        sid = data["header"]["sid"]
        choices = data["payload"]["choices"]
        status = choices["status"]
        content = choices["text"][0]["content"]
        global answer
        answer += content
        # print(1)
        if status == 2:
            ws.close()


def gen_params(appid, domain, question, max_tokens = 4000):
    """
    通过appid和用户的提问来生成请参数
    """
    data = {
        "header": {
            "app_id": appid,
            "uid": "1234"
        },
        "parameter": {

            "chat": {
                "domain": domain,
                "temperature": 0.8,
                "max_tokens": max_tokens,
                "top_k": 5,

                "auditing": "default"
            }
        },
        "payload": {
            "message": {
                "text": question
            }
        }
    }
    return data


def main(appid, api_key, api_secret, Spark_url,domain, question):
    wsParam = Ws_Param(appid, api_key, api_secret, Spark_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()
    ws = websocket.WebSocketApp(wsUrl, on_message=on_message, on_error=on_error, on_close=on_close, on_open=on_open)
    ws.appid = appid
    ws.question = question
    ws.domain = domain
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
