from io import BytesIO
from django.shortcuts import render, redirect, HttpResponse

from app import models
from app.utils import select_api, random_code
from app.form import LoginForm, LogupForm, BlogPublishForm, CommentPublishForm, TransactionForm


def index(request):
    """
    主页
    """

    info = request.session.get('info')

    name = info['name']
    result = {'userinfo_list': []}

    for userinfo in models.select_all('UserInfo'):
        if userinfo.name == name:
            result['userinfo'] = userinfo
        else:
            if userinfo.name in [i.name for i in select_api.select_followinfo_by_username1(name)]:
                pass
            else:
                result['userinfo_list'].append(userinfo)

    result['follows_count'] = len(select_api.select_followinfo_by_username1(name))
    result['fans_count'] = len(select_api.select_followinfo_by_username2(name))

    result['bloginfo_list'] = []
    for bloginfo in models.select_all('BlogInfo'):
        avatar = select_api.select_userinfo_by_name(bloginfo.publisher).avatar
        bloginfo_dict = bloginfo.to_dict()
        bloginfo_dict['avatar'] = avatar
        bloginfo_dict['commentinfo_list'] = [i.to_dict() for i in
                                             select_api.select_commentinfo_by_blogpublisher_and_blogtimestamp(
                                                 bloginfo.publisher, bloginfo.timestamp
                                             )]
        for i in bloginfo_dict['commentinfo_list']:
            i['avatar'] = select_api.select_userinfo_by_name(i['username']).avatar
        bloginfo_dict['likes'] = select_api.select_income_by_username(bloginfo.publisher)
        result['bloginfo_list'].append(bloginfo_dict)
    result['bloginfo_list'].reverse()

    if request.method == 'GET':
        blog_form = BlogPublishForm()
        result['blogform'] = blog_form
        return render(request, 'index.html', result)

    # 若为POST请求
    blog_form = BlogPublishForm(data=request.POST)
    if blog_form.is_valid():
        # 将博客数据保存进rchain中
        models.BlogInfo(
            publisher=name,
            content=blog_form.cleaned_data.get('blog_content'),
            timestamp=select_api.get_timestamp(),
            location='北京',
            likes=0,
            isvalid=True
        ).insert()
        return redirect('/index/')

    return render(request, 'index.html', result)


def comment(request):
    """
    index页面评论
    """

    info = request.session.get('info')

    name = info['name']
    result = {'userinfo_list': []}

    for userinfo in models.select_all('UserInfo'):
        if userinfo.name == name:
            result['userinfo'] = userinfo
        else:
            if userinfo.name in [i.name for i in select_api.select_followinfo_by_username1(name)]:
                pass
            else:
                result['userinfo_list'].append(userinfo)

    result['follows_count'] = len(select_api.select_followinfo_by_username1(name))
    result['fans_count'] = len(select_api.select_followinfo_by_username2(name))

    result['bloginfo_list'] = []
    for bloginfo in models.select_all('BlogInfo'):
        avatar = select_api.select_userinfo_by_name(bloginfo.publisher).avatar
        bloginfo_dict = bloginfo.to_dict()
        bloginfo_dict['avatar'] = avatar
        bloginfo_dict['commentinfo_list'] = [i.to_dict() for i in
                                             select_api.select_commentinfo_by_blogpublisher_and_blogtimestamp(
                                                 bloginfo.publisher, bloginfo.timestamp
                                             )]
        for i in bloginfo_dict['commentinfo_list']:
            i['avatar'] = select_api.select_userinfo_by_name(i['username']).avatar
        bloginfo_dict['likes'] = select_api.select_income_by_username(bloginfo.publisher)
        result['bloginfo_list'].append(bloginfo_dict)
    result['bloginfo_list'].reverse()

    publisher_name = request.GET.get('blog_publisher')
    blog_timestamp = request.GET.get('blog_timestamp')

    if request.method == 'GET':
        blog_form = BlogPublishForm()
        result['blogform'] = blog_form
        comment_form = CommentPublishForm()
        result['commentform'] = comment_form
        return render(request, 'comment.html', result)

    # 若为POST请求
    comment_form = CommentPublishForm(data=request.POST)

    if comment_form.is_valid():
        # 将评论数据保存进rchain中
        models.CommentInfo(
            content=comment_form.cleaned_data.get('comment_content'),
            timestamp=select_api.get_timestamp(),
            username=name,
            blog_to=publisher_name + blog_timestamp,
            isvalid=True
        ).insert()
        return redirect('/index/')

    return render(request, 'comment.html', result)


def transfer(request):
    """
    index页面转账
    """

    info = request.session.get('info')

    name = info['name']
    result = {'userinfo_list': []}

    for userinfo in models.select_all('UserInfo'):
        if userinfo.name == name:
            result['userinfo'] = userinfo
        else:
            if userinfo.name in [i.name for i in select_api.select_followinfo_by_username1(name)]:
                pass
            else:
                result['userinfo_list'].append(userinfo)

    result['follows_count'] = len(select_api.select_followinfo_by_username1(name))
    result['fans_count'] = len(select_api.select_followinfo_by_username2(name))

    result['bloginfo_list'] = []
    for bloginfo in models.select_all('BlogInfo'):
        avatar = select_api.select_userinfo_by_name(bloginfo.publisher).avatar
        bloginfo_dict = bloginfo.to_dict()
        bloginfo_dict['avatar'] = avatar
        bloginfo_dict['commentinfo_list'] = [i.to_dict() for i in
                                             select_api.select_commentinfo_by_blogpublisher_and_blogtimestamp(
                                                 bloginfo.publisher, bloginfo.timestamp
                                             )]
        for i in bloginfo_dict['commentinfo_list']:
            i['avatar'] = select_api.select_userinfo_by_name(i['username']).avatar
        bloginfo_dict['likes'] = select_api.select_income_by_username(bloginfo.publisher)
        result['bloginfo_list'].append(bloginfo_dict)
    result['bloginfo_list'].reverse()

    sender = request.GET.get('sender')
    receiver = request.GET.get('receiver')

    blog_form = BlogPublishForm()
    result['blogform'] = blog_form
    transaction_form = TransactionForm()
    result['transactionform'] = transaction_form

    if request.method == 'GET':
        return render(request, 'transaction.html', result)

    # 若为POST请求
    transaction_form = TransactionForm(data=request.POST)

    if transaction_form.is_valid():
        if int(transaction_form.cleaned_data.get('transaction_amount')) > int(
                select_api.select_userinfo_by_name(name).money):
            transaction_form.add_error('transaction_amount', '用户余额不足，请重新输入！')
            result['transactionform'] = transaction_form
            return render(request, 'transaction.html', result)

        # 将评论数据保存进rchain中
        models.TransactionInfo(
            username1=sender,
            username2=receiver,
            amount=transaction_form.cleaned_data.get('transaction_amount'),
            isvalid=True
        ).insert()
        return redirect('/index/')

    return render(request, 'transaction.html', result)


def follow(request):
    """
    index页面关注功能
    """
    username1 = request.GET.get('username1')
    username2 = request.GET.get('username2')
    models.FollowInfo(
        username1=username1,
        username2=username2,
        isvalid=True
    ).insert()

    return redirect('/index/')


def connection(request):
    """
    关注与粉丝
    """

    info = request.session.get('info')

    name = info['name']
    result = {'userinfo': select_api.select_userinfo_by_name(name),
              'follows_count': len(select_api.select_followinfo_by_username1(name)),
              'fans_count': len(select_api.select_followinfo_by_username2(name)),
              "followers": select_api.select_followinfo_by_username1(name),
              "followings": select_api.select_followinfo_by_username2(name)}

    return render(request, 'connection.html', result)


def profile(request):
    """
    个人主页
    """

    info = request.session.get('info')

    name = info['name']
    result = {'userinfo': select_api.select_userinfo_by_name(name),
              'follows_count': len(select_api.select_followinfo_by_username1(name)),
              'fans_count': len(select_api.select_followinfo_by_username2(name)),
              'bloginfo_list': select_api.select_bloginfo_by_publisher(name),
              'fans_list': select_api.select_followinfo_by_username2(name)}
    result['bloginfo_list'].reverse()

    return render(request, 'profile.html', result)


def sign_in(request):
    """
    登录
    """

    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'sign-in.html', {'form': form})

    # 若为POST请求，验证表单数据
    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 验证成功
        user_input_code = form.cleaned_data['code']
        code = request.session.get('image_code')
        if code.upper() != user_input_code.upper():
            form.add_error('code', '验证码错误')
            return render(request, 'sign-in.html', {'form': form})

        admin_object = select_api.select_userinfo_by_name(form.cleaned_data['username'])
        if not admin_object:
            # 用户名不存在
            form.add_error('password', '用户名或密码错误')
            return render(request, 'sign-in.html', {'form': form})

        if admin_object.password != form.cleaned_data['password']:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'sign-in.html', {'form': form})

        request.session['info'] = {'name': admin_object.name}
        return redirect('/index/')

    # 验证失败
    return render(request, 'sign-in.html', {'form': form})


def sign_up(request):
    """
    注册
    """

    if request.method == 'GET':
        form = LogupForm()
        return render(request, 'sign-up.html', {'form': form})

    # 若为POST请求
    form = LogupForm(data=request.POST)
    if form.is_valid():
        # 将用户数据保存进rchain中
        models.UserInfo(
            name=form.cleaned_data.get('username'),
            password=form.cleaned_data.get('password'),
            money=100,
            intro='你好，我是' + form.cleaned_data.get('username') + '！',
            avatar=select_api.get_random_avatar(),
            label='IT',
            isvalid=1
        ).insert()
        return redirect('/sign-in/')

    return render(request, 'sign-up.html', {'form': form})


def logout(request):
    """
    注销
    """
    request.session.clear()
    return redirect('/sign-in/')


def code(request):
    img, code = random_code.check_code()

    request.session['image_code'] = code

    # 写入内存
    stream = BytesIO()
    img.save(stream, 'png')

    return HttpResponse(stream.getvalue())


if __name__ == '__main__':
    print(select_api.get_random_avatar())
