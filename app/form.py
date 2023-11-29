from django import forms
from django.core.exceptions import ValidationError

from app.utils import select_api


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        required=True,
    )
    code = forms.CharField(
        label='验证码',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )


class LogupForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        required=True,
    )
    password_confirm = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}, render_value=True),
        required=True,
    )

    def clean_username(self):
        name = self.cleaned_data.get('username')
        if select_api.select_userinfo_by_name(name):
            raise ValidationError("用户名已存在，请重新输入！")
        return name

    def clean_password_confirm(self):
        pwd = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('password_confirm')
        if pwd != confirm:
            raise ValidationError('密码不一致，请重新输入！')
        return confirm


class BlogPublishForm(forms.Form):
    blog_content = forms.CharField(
        label='内容',
        widget=forms.Textarea(
            attrs={'class': 'form-control border-0 p-0 shadow-none',
                   'rows': '1',
                   'id': 'home_textarea',
                   'placeholder': '写下你的想法...... '}
        ),
        required=True,
    )


class CommentPublishForm(forms.Form):
    comment_content = forms.CharField(
        label='内容',
        widget=forms.Textarea(
            attrs={'class': 'comment_text',
                   'id': 'comment_text',
                   'placeholder': '写下你的评论... '}
        ),
        required=True,
    )


class TransactionForm(forms.Form):
    transaction_amount = forms.CharField(
        label='金额',
        widget=forms.Textarea(
            attrs={'class': 'comment_text',
                   'style': 'height: 40px;',
                   'id': 'comment_text',
                   'placeholder': '输入你想赞赏的金额...'}
        ),
        required=True,
    )
