# 1.2
# import time
#以下密钥信息从控制台获取   https://console.xfyun.cn/services/bm35

class 认证信息:
    """
    你需要注册讯飞星火的账号,购买讯飞星火产品,\n
    并从https://console.xfyun.cn/services/cbm 
    获取你的appid, api_secret, api_key并在创建实例时填写进来\n
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
        初始化星火消息
        最大字符长度 -> 请在官方文档中查看你使用的版本支持的最大token数来修改这个\n
        你需要先创建一个 **认证信息** 实例, 再创建一个星火消息\n
        星火消息在调用SparkApi时,默认情况下将会使用Spark Lite版本\n
        .\n
        ### **下面是星火消息提供的函数**\n
        **更改ai设定** -> 修改ai的设定\n
        **置最大字符长度** -> 所有消息加起来的字符总数将不超过此数字, 默认8000\n
        **置消息历史** -> 插入历史消息,role为该消息发送的对象, 通常可以不使用此项而是使用另外两项\n
        **获取回复** -> 调用官方文档向ai发送星火消息的内容并获取回复\n
        **置用户消息到历史** -> 向星火消息内加入用户的消息, 最新一次添加的消息将被判定为ai要回复的内容\n
        **置入ai回复到历史** -> 目前在默认情况下会自动置入ai回复\n
        **取历史消息总长度** -> 取所有历史消息的总字符数\n
        **检查消息长度并处理** -> 如果超出了 *最大字符长度* 的限制, 它将删除最早的历史消息,如果仍然超出,它将删除设定.建议开发者调用时不要允许用户发送超过(最大字符长度-设定文本的长度)\n
        **调用的ai版本** -> 用于更改调用的讯飞星火大模型版本, 已经加入了文档中提供的所有大模型版本\n
        **自动置历史回复** -> 开关自动置入ai回复的函数, 如果关闭该功能, ai将不会参考历史中它自己的回复 **(该功能被设计为关闭历史消息选项, 但是并未完善, 不建议关闭该功能)**
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
            # self.检查消息长度并处理()

        新消息 = {"role": "user", "content": self.新消息}
        总消息.append(新消息)

        # print(self.消息)
        self.api.answer = ""
        self.api.main(总消息)

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
        你可以选择以下的数字: 0,1,2,3,4,5\n
        0 -> Spark Lite\n
        1 -> Spark V2.0\n
        2 -> Spark Pro \n
        3 -> Spark Pro-128K\n
        4 -> Spark Max \n
        5 -> Spark4.0 Ultra \n
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
    def __init__(self, 认证信息:认证信息, Spark_url, domain):
        self.answer = ""
        self.sid = ''
        self.ws参数 = ws参数(认证信息, Spark_url)
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp("", on_message=self.on_message, on_error=self.on_error, on_close=self.on_close, on_open=self.on_open)
        self.appid = 认证信息.appid
        self.domain = domain


    # 收到websocket错误的处理
    def on_error(self, ws , error):
        print("### error:", error)
    
    
    # 收到websocket关闭的处理
    def on_close(self, ws, one,two):
        pass
    
    
    # 收到websocket连接建立的处理
    def on_open(self, ws):
        thread.start_new_thread(self.run, ())
    
    
    def run(self, *args):
        data = json.dumps(
            self.gen_params(
                 appid=self.appid
                ,domain= self.domain
                ,question=self.question
                )
            )
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
    
    
    def gen_params(self, appid, domain, question):
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
                    "max_tokens": 4096,
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