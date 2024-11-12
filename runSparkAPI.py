# 1.2.1
# 使用python3.12编写

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
        self.appid = APPID 
        self.api_secret = APISecret   
        self.api_key = APIKey


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
        self.ID = ID
        self.调用的ai版本(0)         
        self.最大字符长度 = 最大字符长度
        self.自动置历史 = True
        self.api = SparkAPI(ID, self.Spark_url, self.domain)
    
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
        ) -> str :
        
        总消息 = [self.设定]
        if 使用历史回复 :
            总消息 += self.历史
            self.检查消息长度并处理()

        新消息 = {"role": "user", "content": self.新消息}
        总消息.append(新消息)

        # print(self.消息)
        self.api.answer = "" # 重置回复信息
        self.api.main(总消息)# 获取回复

        回复 = self.api.answer

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

# 以下代码修改自讯飞星火官方文档
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


class SparkAPI():
    """
    SparkAPI类用于与Spark的WebSocket API进行交互。它提供了初始化连接、发送问题、接收回答等功能。通常可以不使用SparkAPI类
    
    Parameters:
        认证信息 (object): 包含appid等信息的认证对象。
        Spark_url (str): Spark WebSocket API的URL。
        domain (str): 指定大模型版本，例如'generalv2.5'。
    
    Attributes:
        answer (str): 存储从Spark API接收到的回答。
        sid (str): 会话ID，用于跟踪特定的对话。
        ws参数 (object): 包含WebSocket连接所需的参数的对象。
        ws (object): WebSocketApp实例，用于建立和管理WebSocket连接。
        appid (str): 应用程序的ID，用于认证和识别。
        domain (str): 大模型版本。
    
    Methods:
        on_error(ws, error): 当WebSocket发生错误时调用的处理函数。
        on_close(ws, one, two): 当WebSocket关闭时调用的处理函数。
        on_open(ws): 当WebSocket连接打开时调用的处理函数。
        run(*args): 在新线程中运行，向WebSocket发送请求并处理响应。
        on_message(ws, message): 当从WebSocket接收到消息时调用的处理函数。
        gen_params(appid, domain, question): 根据appid和用户的提问生成请求参数。
        main(question): 主函数，用于启动WebSocket连接并发送问题。
    """
    def __init__(self, 认证信息:认证信息, Spark_url, domain, max_tokens=4096):
        self.answer = ""
        self.sid = ''
        self.ws参数 = ws参数(认证信息, Spark_url)
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp("", on_message=self.on_message, on_error=self.on_error, on_close=self.on_close, on_open=self.on_open)
        self.appid = 认证信息.appid
        self.domain = domain
        self.max_tokens = max_tokens


    # 收到websocket错误的处理
    def on_error(self, ws , error):
        print("### error:", error)
    
    
    # 收到websocket关闭的处理
    def on_close(self, ws, one, two):
        pass
    
    
    # 收到websocket连接建立的处理
    def on_open(self, ws):
        thread.start_new_thread(self.run, ())
    
    
    def run(self, *args):
        data = json.dumps(self.gen_params())
        self.ws.send(data)
    
    
    # 收到websocket消息的处理
    def on_message(self,ws, message):
        # print(message)
        # print(time.time())
        data = json.loads(message)
        code = data['header']['code']
        if code != 0:
            print(f'请求错误: {code}, {data}')
            self.ws.close()
        else:
            self.sid = data["header"]["sid"]
            choices = data["payload"]["choices"]
            status = choices["status"]
            content = choices["text"][0]["content"]
            
            self.answer += content
            # print(1)
            if status == 2:
                self.ws.close()
    
    
    def gen_params(self):
        """
        通过appid和用户的提问来生成请参数
        """
        data = {
            "header": {
                "app_id": self.appid,
                "uid": "1234"
            },
            "parameter": {
    
                "chat": {
                    "domain": self.domain,
                    "temperature": 0.8,
                    "max_tokens": self.max_tokens,
                    "top_k": 5,
    
                    "auditing": "default"
                }
            },
            "payload": {
                "message": {
                    "text": self.question
                }
            }
        }
        return data


    def main(self, question):
        self.answer = ""
        wsUrl = self.ws参数.生成url()
        self.ws.url = wsUrl
        self.question = question
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        



class ws参数(object):
    # 初始化
    def __init__(self, 认证信息: 认证信息, Spark_url:str):
        self.APPID     = 认证信息.appid
        self.APIKey    = 认证信息.api_key
        self.APISecret = 认证信息.api_secret
        self.host = urlparse(Spark_url).netloc
        self.path = urlparse(Spark_url).path
        self.Spark_url = Spark_url

    # 生成url
    def 生成url(self):
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