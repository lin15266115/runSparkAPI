**该程序提供了来自这里的代码：**

https://www.xfyun.cn/doc/spark/Web.html#_3-%E8%B0%83%E7%94%A8%E7%A4%BA%E4%BE%8B 里面的 “python 带上下文调用示例” 

## **这个程序创建了**两个类：**认证信息** 和 **星火消息**
### 认证性息 ：*用于保存星火接口的认证信息*

你需要注册讯飞星火的账号,购买讯飞星火产品,
并从https://console.xfyun.cn/services/cbm 
获取你的appid, api_secret, api_key并在创建实例时填写进来:

    key = 认证信息（
     APPID = ""
    ,APISecret = ""
    ,APIKey = ""
    ）

### 星火消息 : *用于保存向AI发送的所有必要信息*
***更改ai设定*** -> 修改ai的设定.

***置最大字符长度*** -> 所有消息加起来的字符总数将不超过此数字, 默认8000.

***置消息历*史** -> 插入历史消息,role为该消息发送的对象, 通常可以不使用此项而是使用另外两项.

***获取回复*** -> 调用官方文档向ai发送星火消息的内容并获取回复.

***置用户消息到历史*** -> 向历史消息内加入用户的消息, 最新一次添加的消息将被判定为ai要回复的内容.

***置入ai回复到历史*** -> 目前在默认情况下会自动置入ai回复到历史.

***取历史消息总长度*** -> 取所有历史消息的总字符数.

***检查消息长度并处理*** -> 如果超出了*最大字符长度* 的限制, 它将删除最早的历史消息,如果仍然超出,它将删除设定.建议开发者调用时不要允许用户发送超过(最大字符长度-设定文本的长度).

***调用的ai版本*** -> 用于更改调用的讯飞星火大模型版本, 已经加入了文档中提供的所有大模型版本.

***自动置历史回复*** -> 开关自动置历史回复的函数, 如果关闭该功能, 星火消息将不会自动将消息记录保存到历史中.

#### *值的介绍*

 ***设定** 保存为一个键值对*

    self.设定 = {"role": "system", "content": ""}
***历史** 保存为一个列表, 里面用于存储历史消息,这些消息以键值对形式保存.*

    self.历史 = []
***新消息** 保存为一个字符串, 在调用 获取回复( ) 时它会作为最新向AI发送的消息插入到向AI发送的消息内*

    self.新消息 = ""
#### 调用示例:

    import runSparkAPI

    key = runSparkAPI.认证信息（
         APPID = ""
        ,APISecret = ""
        ,APIKey = ""
    ）
    
    abc = runSparkAPI.星火消息(key) 
     # 创建一个星火消息实例,key为上面创建的 认证性息 实例
    abc.更改ai设定("你是一个智能机器人,你叫123465789,正在参与一个测试")
     # 修改AI的设定
    while True :
        c = input("\n我:") # 在控制台获取用户的回复
        abc.新消息 = c
         # 更改新消息内容
        回复 = abc.获取回复()
         # 获取回复
        print(回复)
         # 打印回复
