import time
import re
import base64

from rchain.client import RClient
from rchain.util import create_deploy_data, verify_deploy_data
from rchain.crypto import PrivateKey

private_key = PrivateKey.from_hex('75b2093b371e480a368e87655b6bdf1eea648c58f016ef78b11d72237bed7976')  # 私钥
public_key = private_key.get_public_key()  # 公钥
ip = '127.0.0.1'  # ip
port = 40402  # 端口


def return_data_list() -> list[str]:
    """
    返回已部署数据
    """
    with RClient(ip, port) as client:
        blockhash_list = [i.blockHash for i in client.get_blocks_by_heights(
            start_block_number=1,
            end_block_number=client.show_blocks()[0].blockNumber
        )
                          ]
        data_list = []
        for i in blockhash_list:
            block_info = client.show_block(i)
            data = extract_quotes(block_info.deploys[0].term)
            data_list.append(data[0])

    return data_list


def extract_quotes(string: str) -> list[str]:
    """
    正则表达式提取数据
    """
    pattern = r"!\(\"(.*?)\"\)"
    quotes = re.findall(pattern, string)
    return quotes


def func_deploy(rho_code: str) -> str:
    """
    智能合约的部署
    :param rho_code: 合约内容（str）
    :return: 返回读取到的数据
    """
    timestamp = int(time.time()) * 1000  # 时间戳

    client = RClient(ip, port)

    unforgeable_name = client.previewPrivateNames(public_key, timestamp, 1)  # 唯一名称
    print('Prepare Deploy...' + '\n')
    print('UnforgeableName:')
    print(unforgeable_name.payload, end='\n')

    valid_after_block_number = client.show_blocks()[0].blockNumber  # 最新区块

    deploy_data = create_deploy_data(
        timestamp_millis=timestamp,
        term=rho_code,
        key=private_key,
        phlo_limit=100000,
        phlo_price=1,
        valid_after_block_no=valid_after_block_number
    )

    verify_deploy_data(key=public_key, sig=deploy_data.sig, data=deploy_data)

    deploy_id = client.send_deploy(deploy_data)  # 部署
    print('deployResponse:')
    print('Success!')
    print('deployId:' + deploy_id + '\n')

    client.propose()
    print('Propose...' + '\n')

    time.sleep(3)  # 等待部署结果
    print('Propose Success!' + '\n')

    light_blockinfo = client.find_deploy(deploy_id)  # 返回部署结果
    print('DeployInfo:')
    print(light_blockinfo)

    ret = ''

    blockinfo = client.show_block(light_blockinfo.blockHash)
    data = extract_quotes(blockinfo.deploys[0].term)
    print('data:')
    print(data[0] + '\n')

    ret = data[0]  # 提取到的数据

    print('Deploy Finished!\n')
    return ret


def func_deploy_fromfile(rho_file: str) -> str:
    """
    智能合约的部署（文件版本）
    :param rho_file: 智能合约文件
    :return: 返回读取到的数据
    """
    with open(rho_file, 'r') as f:
        rho_code = f.read()
    return func_deploy(rho_code)


def select() -> list[str]:
    """
    查找数据
    :return: 返回数据列表
    """
    # time.sleep(2)
    data_list = return_data_list()
    return data_list


def insert(str_to_insert: str) -> None:
    """
    插入数据
    :param str_to_insert: 需要插入的数据
    :return: None
    """
    contract = '''
    new getInfo, setInfo in {{
        @{{"global_factory"}}!(*getInfo, *setInfo)
        |
        setInfo!("{}")
    }}
    '''.format(str_to_insert)

    func_deploy(contract)


class UserInfo(object):
    """
    用户信息类
    """

    def __init__(self, name: str, password: str, money: int, intro: str, label: str, avatar: str, isvalid: int) -> None:
        """
        构造函数
        :param name:  # 用户名（主键）
        :param password:  # 密码
        :param money:  # 钱包
        :param intro:  # 个人介绍
        :param label:  # 标签
        :param avatar:  # 头像
        :param isvalid:  # 是否有效（1：有效，0：无效）
        """
        self.name = name
        self.password = password
        self.money = money
        self.intro = intro
        self.label = label
        self.avatar = avatar
        self.isvalid = isvalid

    def insert(self) -> bool:
        """
        将用户信息插入rchain中
        :return: 是否插入成功
        """
        # userinfo_list = select_all('UserInfo')
        #
        # for userinfo in userinfo_list:
        #     if userinfo.name == self.name:
        #         return False

        # 合约字符串
        contract_str = (
            f'UserInfo('
            f'name:={self.name}##'
            f'password:={self.password}##'
            f'money:={self.money}##'
            f'intro:={self.intro}##'
            f'label:={self.label}##'
            f'avatar:={self.avatar}##'
            f'isvalid:={self.isvalid}'
            f')'
        )
        insert(contract_str)
        return True

    def __str__(self) -> str:
        """
        重写str方法，打印用户信息具体内容
        """
        return f'UserInfo(name:{self.name}, password:{self.password}, money:{self.money}, intro:{self.intro}, label:{self.label}, avatar:{self.avatar}, isvalid:{self.isvalid})'

    def to_dict(self) -> dict:
        """
        将用户信息转化为字典形式
        """
        return {
            'name': self.name,
            'password': self.password,
            'money': self.money,
            'intro': self.intro,
            'label': self.label,
            'avatar': self.avatar,
            'isvalid': self.isvalid
        }


class BlogInfo(object):
    """
    博客信息类
    """

    def __init__(self, publisher: str, content: str, timestamp: str, location: str, likes: int, isvalid: int) -> None:
        """
        构造函数（博客发布者+时间戳作为主键）
        :param publisher: 博客发布者
        :param content: 博客内容
        :param timestamp: 时间
        :param location: 地点
        :param likes: 获赞数
        :param isvalid: 是否有效（1：有效，0：无效）
        """
        self.publisher = publisher
        self.content = content
        self.timestamp = timestamp
        self.location = location
        self.likes = likes
        self.isvalid = isvalid

    def insert(self) -> bool:
        """
        将博客信息插入rchain中
        :return: 是否插入成功
        """

        # bloginfo_list = select_all('BlogInfo')
        # for bloginfo in bloginfo_list:
        #     if bloginfo.publisher == self.publisher and bloginfo.timestamp == self.timestamp:
        #         return False

        # 合约字符串
        contract_str = (
            f'BlogInfo('
            f'publisher:={self.publisher}##'
            f'content:={self.content}##'
            f'timestamp:={self.timestamp}##'
            f'location:={self.location}##'
            f'likes:={self.likes}##'
            f'isvalid:={self.isvalid}'
            f')'
        )
        insert(contract_str)
        return True

    def __str__(self) -> str:
        """
        重写str方法，打印博客信息具体内容
        """
        return f'BlogInfo(publisher:{self.publisher}, content:{self.content}, timestamp:{self.timestamp}, location:{self.location}, likes:{self.likes}, isvalid:{self.isvalid})'

    def to_dict(self):
        """
        将博客信息转化为字典形式
        """
        return {
            'publisher': self.publisher,
            'content': self.content,
            'timestamp': self.timestamp,
            'location': self.location,
            'likes': self.likes,
            'isvalid': self.isvalid
        }


class CommentInfo(object):
    """
    评论信息类
    """

    def __init__(self, content: str, timestamp: str, username: str, blog_to: str, isvalid: int) -> None:
        """
        构造函数（评论人+对应推文+时间戳为主键）
        :param content: 评论内容
        :param timestamp: 时间戳
        :param username: 评论人
        :param blog_to: 对应推文（采用“推文发布者+时间戳”的形式）
        :param isvalid: 是否有效（1：有效，0：无效）
        """
        self.content = content
        self.timestamp = timestamp
        self.username = username
        self.blog_to = blog_to
        self.isvalid = isvalid

    def insert(self) -> bool:
        """
        将评论信息插入rchain中
        :return: 是否插入成功
        """

        # 合约字符串
        contract_str = (
            f'CommentInfo('
            f'content:={self.content}##'
            f'timestamp:={self.timestamp}##'
            f'username:={self.username}##'
            f'blog_to:={self.blog_to}##'
            f'isvalid:={self.isvalid}'
            f')'
        )
        insert(contract_str)
        return True

    def __str__(self) -> str:
        """
        重写str方法，打印评论信息具体内容
        """
        return f'CommentInfo(content:{self.content}, timestamp:{self.timestamp}, username:{self.username}, blog_to:{self.blog_to}. isvalid:{self.isvalid})'

    def to_dict(self):
        """
        将评论信息转化为字典形式
        """
        return {
            'content': self.content,
            'timestamp': self.timestamp,
            'username': self.username,
            'blog_to': self.blog_to,
            'isvalid': self.isvalid
        }


class FollowInfo(object):
    """
    关注信息类
    单向关注，username1关注username2
    """

    def __init__(self, username1: str, username2: str, isvalid: int) -> None:
        """
        构造函数（关注人+被关注人为主键）
        :param username1: 用户1
        :param username2: 用户2
        """
        self.username1 = username1
        self.username2 = username2
        self.isvalid = isvalid

    def insert(self) -> bool:
        """
        将关注信息插入rchain中
        :return: 是否插入成功
        """
        contract_str = (
            f'FollowInfo('
            f'username1:={self.username1}##'
            f'username2:={self.username2}##'
            f'isvalid:={self.isvalid}'
            f')'
        )
        insert(contract_str)
        return True

    def __str__(self) -> str:
        """
        重写str方法，打印关注信息具体内容
        """
        return f'FollowInfo(username1:{self.username1}, username2:{self.username2}, isvalid:{self.isvalid})'


def parse_string(string: str, start_str: str) -> dict:
    """
    将从rchain中读取的信息字符串解析为字典形式
    :param string: 从rchain中读取的信息字符串
    :param start_str: 内容类别（UserInfo、BlogInfo、CommentInfo、FollowInfo）
    """
    dictionary = {}
    n = len(start_str)
    temp_list = string[n + 1:][:-1].split('##')
    for item in temp_list:
        key, value = item.split(":=")
        dictionary[key] = value
    return dictionary


def select_all(data: str) -> list:
    """
    从rchain中读取某一类别（UserInfo、BlogInfo、CommentInfo、FollowInfo）的所有信息
    :param data: 类别
    :return: 信息列表，每个元素为一个类的实例
    """

    data_list = select()
    data_list_class = []
    if data == 'UserInfo':
        data_list_cleaned = [parse_string(i, 'UserInfo') for i in data_list if i.startswith('UserInfo')]
        data_list_class = [
            UserInfo(i['name'], i['password'], i['money'], i['intro'], i['label'], i['avatar'], i['isvalid'])
            for i in data_list_cleaned
        ]
    elif data == 'BlogInfo':
        data_list_cleaned = [parse_string(i, 'BlogInfo') for i in data_list if i.startswith('BlogInfo')]
        data_list_class = [
            BlogInfo(i['publisher'], i['content'], i['timestamp'], i['location'], i['likes'], i['isvalid'])
            for i in data_list_cleaned
        ]
    elif data == 'CommentInfo':
        data_list_cleaned = [parse_string(i, 'CommentInfo') for i in data_list if i.startswith('CommentInfo')]
        data_list_class = [
            CommentInfo(i['content'], i['timestamp'], i['username'], i['blog_to'], i['isvalid'])
            for i in data_list_cleaned
        ]
    elif data == 'FollowInfo':
        data_list_cleaned = [parse_string(i, 'FollowInfo') for i in data_list if i.startswith('FollowInfo')]
        data_list_class = [
            FollowInfo(i['username1'], i['username2'], i['isvalid'])
            for i in data_list_cleaned
        ]

    return data_list_class


if __name__ == '__main__':
    # 测试用户数据插入
    with open('../app/static/img/p1.png', 'rb') as f:
        image_binary = f.read()
        image_base64 = base64.b64encode(image_binary).decode('utf-8')
        user_xiaozhe = UserInfo('小哲同学', 'xiaozhe123', 100, '你好，我是小哲同学', 'IT', image_base64, 1)
        user_xiaozhe.insert()
    with open('../app/static/img/p2.png', 'rb') as f:
        image_binary = f.read()
        image_base64 = base64.b64encode(image_binary).decode('utf-8')
        user_kongdu = UserInfo('空渡', 'kongdu123', 100, '你好，我是空渡', 'IT', image_base64, 1)
        user_kongdu.insert()
    with open('../app/static/img/p3.png', 'rb') as f:
        image_binary = f.read()
        image_base64 = base64.b64encode(image_binary).decode('utf-8')
        user_shuizhongyue = UserInfo('水中月', 'shuizhongyue123', 100, '你好，我是水中月', 'IT', image_base64, 1)
        user_shuizhongyue.insert()
    with open('../app/static/img/p4.png', 'rb') as f:
        image_binary = f.read()
        image_base64 = base64.b64encode(image_binary).decode('utf-8')
        user_exm = UserInfo('?.exm.?', '?.exm.?123', 100, '你好，我是?.exm.?', 'IT', image_base64, 1)
        user_exm.insert()

    # 测试博客插入
    blog1_xiaozhe = BlogInfo(
        '小哲同学',
        "这是小哲同学的第一篇博客。",
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        '北京',
        0,
        1
    )
    blog1_xiaozhe.insert()
    blog2_xiaozhe = BlogInfo(
        '小哲同学',
        "这是小哲同学的第二篇博客。",
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        '北京',
        0,
        1
    )
    blog2_xiaozhe.insert()
    blog3_xiaozhe = BlogInfo(
        '小哲同学',
        "这是小哲同学的第三篇博客。",
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        '北京',
        0,
        1
    )
    blog3_xiaozhe.insert()
    blog1_kongdu = BlogInfo(
        '空渡',
        "这是空渡的第一篇博客。",
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        '北京',
        0,
        1
    )
    blog1_kongdu.insert()

    # 测试关注信息插入
    follow_xiaozhe_kongdu = FollowInfo('小哲同学', '空渡', 1)
    follow_xiaozhe_kongdu.insert()
    follow_kongdu_xiaozhe = FollowInfo('空渡', '小哲同学', 1)
    follow_kongdu_xiaozhe.insert()
    follow_shuizhongyue_xiaozhe = FollowInfo('水中月', '小哲同学', 1)
    follow_shuizhongyue_xiaozhe.insert()
    follow_exm_xiaozhe = FollowInfo('?.exm.?', '小哲同学', 1)
    follow_exm_xiaozhe.insert()

    # 测试评论信息插入
    comment1_xiaozhe_blog1 = CommentInfo(
        '这是小哲同学的第一篇博客的第一条评论。',
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        '小哲同学',
        blog1_xiaozhe.publisher + blog1_xiaozhe.timestamp,
        1
    )
    comment1_xiaozhe_blog1.insert()

    # # 打印插入数据信息
    # print('#' * 30)
    # for i in select_all('UserInfo'):
    #     print(i)
    # print('#' * 30)
    # for i in select_all('BlogInfo'):
    #     print(i)
    # print('#' * 30)
    # for i in select_all('CommentInfo'):
    #     print(i)
    # print('#' * 30)
    # for i in select_all('FollowInfo'):
    #     print(i)
