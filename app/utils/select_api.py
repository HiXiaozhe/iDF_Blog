import time
import random
import base64

from app import models


def select_userinfo_by_name(name: str) -> models.UserInfo:
    """
    通过用户名从UserInfo中查询用户信息
    :param name: 用户名
    :return: 用户信息
    """
    for userinfo in models.select_all('UserInfo'):
        if userinfo.name == name:
            userinfo.money = int(userinfo.money) + select_income_by_username(name) - select_outcome_by_username(name)
            return userinfo


def select_bloginfo_by_publisher(publisher: str) -> list[models.BlogInfo]:
    """
    通过用户名从BlogInfo中查询用户信息
    :param publisher: 用户名
    :return: 博客信息列表
    """
    bloginfo_list = []
    for bloginfo in models.select_all('BlogInfo'):
        if bloginfo.publisher == publisher:
            bloginfo_list.append(bloginfo)
    return bloginfo_list


def select_followinfo_by_username2(username2: str) -> list[models.UserInfo]:
    """
    通过用户名从FollowInfo中查询粉丝信息
    谁关注了username2
    :param username2: 用户名
    :return: 粉丝信息列表
    """
    userinfo_list = []
    for followinfo in models.select_all('FollowInfo'):
        if followinfo.username2 == username2:
            userinfo_list.append(select_userinfo_by_name(followinfo.username1))
    return userinfo_list


def select_followinfo_by_username1(username1: str) -> list[models.UserInfo]:
    """
    通过用户名从FollowInfo中查询关注信息
    username1关注了谁
    :param username1: 用户名
    :return: 关注用户信息列表
    """
    userinfo_list = []
    for followinfo in models.select_all('FollowInfo'):
        if followinfo.username1 == username1:
            userinfo_list.append(select_userinfo_by_name(followinfo.username2))
    return userinfo_list


def select_commentinfo_by_blogpublisher_and_blogtimestamp(blog_publisher: str, blog_timestamp: str) \
        -> list[models.CommentInfo]:
    commentinfo_list = []
    for commentinfo in models.select_all('CommentInfo'):
        if commentinfo.blog_to == blog_publisher + blog_timestamp:
            commentinfo_list.append(commentinfo)
    return commentinfo_list


def select_followuserinfo_by_username1(username1: str):
    """
    通过用户名从FollowUserInfo中查询关注信息
    username1关注了谁
    :param username1: 用户名
    :return: 关注用户信息列表
    """
    userinfo_list = []
    for followinfo in models.select_all('FollowInfo'):
        if followinfo.username1 == username1:
            userinfo_list.append(select_userinfo_by_name(followinfo.username2))
    return userinfo_list


def select_income_by_username(username2: str) -> int:
    """
    通过用户名查询用户收入
    :param username2: 用户名
    :return: 收入
    """

    income = 0
    for transactioninfo in models.select_all('TransactionInfo'):
        if transactioninfo.username2 == username2:
            income += int(transactioninfo.amount)
    return income


def select_outcome_by_username(username1: str) -> int:
    """
    通过用户名查询用户支出
    :param username1: 用户名
    :return: 支出
    """
    outcome = 0
    for transactioninfo in models.select_all('TransactionInfo'):
        if transactioninfo.username1 == username1:
            outcome += int(transactioninfo.amount)
    return outcome


def get_timestamp() -> str:
    """
    获取时间戳
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_random_avatar() -> str:
    """
    获取随机头像
    """
    rand = random.randint(1, 10)
    print(rand)
    path = 'app/static/img/p' + str(rand) + '.png'
    with open(path, 'rb') as f:
        image_binary = f.read()
        image_base64 = base64.b64encode(image_binary).decode('utf-8')

    return image_base64


if __name__ == '__main__':
    # models.TransactionInfo('空渡', '小哲同学', 10, 1).insert()
    # print(select_income_by_username('小哲同学'))
    # print(select_outcome_by_username('小哲同学'))
    # print(select_userinfo_by_name('小哲同学').money)
    print(get_random_avatar())