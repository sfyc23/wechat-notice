# -*- coding: utf-8 -*-
"""
Project: wechat-notice
Creator: DoubleThunder
Create time: 2019-10-08 10:23
Introduction:
"""
import yagmail
import requests

class WechatNotice(object):
    return_success = {'isSuccess': True, 'msg': ''}
    return_fail = {'isSuccess': False, 'msg': '未知'}

    def send(self, title, content, receivers=''):
        raise NotImplementedError()


class EmailNotice(WechatNotice):
    """
    notice = EmailNotice(user="token", password='',
                                host='',to_emails=['1@163.com','2@qq.com'])
    notice.send('title','content')
    你需要安装 yagmail 才能使用
    """
    to_emails = []
    def __init__(self, user, password, host, to_emails=None):

        self.mail_conn = yagmail.SMTP(user=user, password=password, host=host)
        if to_emails:
            self.to_emails = to_emails

    def send(self, title='', content='', receivers=None):
        """
        :param title: str, 消息标题，最长为 256，必填。
        :param content: str, 消息内容，最长 64 Kb，可空，支持 MarkDown。
        :return: bool, True 发送成功；False,发送成功。
        """
        if receivers:
            to_receivers = receivers
        elif self.to_emails:
            to_receivers = self.to_emails
        else:
            self.return_fail['msg'] = '请输入要发送的邮箱'
            return self.return_fail

        try:
            self.mail_conn.send(to_receivers, title, content)
            return self.return_success
        except Exception as exception:
            # print(str(exception))
            self.return_fail['msg'] = str(exception)
            return self.return_fail

class ServerChanNotice(WechatNotice):
    """
    Server 酱 ——「程序员」和「服务器」之间的通信软件。(一对多：PushBear)
    官网：http://sct.ftqq.com
    使用：
    notice = ServerChanNotice(sckey='你申请的sckey')
    notice.send('这是一个标题','这是内容')
    需要安装 requests 才可使用。
    """

    base_url = 'https://sctapi.ftqq.com/{sckey}.send'
    url = None

    def __init__(self, sckey=None):
        if sckey:
            self.url = self.base_url.format(sckey=sckey)

    def send(self, title='', content='', receivers=''):
        """
        :param title: str, 消息标题，最长为 256，必填。
        :param content: str, 消息内容，最长 64 Kb，可空，支持 MarkDown。
        :param receivers: str ,（可空）需要发送的 sckey。如果初始化时有定义，则不需要填写
        :return: {'isSuccess': False, 'msg': '错误原因'}
        """
        if receivers:
            send_url = self.base_url.format(sckey=receivers)
        elif self.url:
            send_url = self.url
        else:
            self.return_fail['msg'] = 'sckey 不能为空！'
            return self.return_fail

        if not title or not title.strip():
            title = '无标题'

        elif len(title) >= 256:
            title = title[:256]
        payload = {'text': title, 'desp': content}
        try:
            resp = requests.get(send_url, params=payload)
            if resp.status_code == 200:
                # print(resp.text)
                content_dict = resp.json()
                if content_dict['errno'] == 0:
                    # print('发送成功')
                    return self.return_success
                else:
                    self.return_fail['msg'] = content_dict['errmsg']
                    return self.return_fail
            self.return_fail['msg'] = '网络请求失败'
            return self.return_fail
        except Exception as exception:
            self.return_fail['msg'] = str(exception)
            return self.return_fail


class NiucodataChanNotice(WechatNotice):
    """
    推了噜 ——无需编写代码，1分钟实现表单推送至微信

    官网：https://m.niucodata.com/tui
    使用：
    notice = NiucodataChanNotice(openid='你申请的openid')
    notice.send('这是一个标题','这是内容')
    需要安装 requests 才可使用。
    """
    __URL__ = 'https://m.niucodata.com/yo'
    def __init__(self, openid=None):
        if openid:
            self.openid = openid

    def send(self, title='', content='', receivers=''):
        """
        :param title: str, 消息标题，最长为 256，必填。
        :param content: str||dict, 消息内容，可以为 dict
        :param receivers: str ,（可空）需要发送的 openid。如果初始化时有定义，则不需要填写
        :return: {'isSuccess': False, 'msg': '错误原因'}
        """
        if receivers:
            send_openid = receivers
        elif self.openid:
            send_openid = self.openid
        else:
            self.return_fail['msg'] = 'openid 不能为空！'
            return self.return_fail

        if not title or not title.strip():
            title = '无标题'

        if isinstance(content, str):
            data = {'正文': content}
        elif isinstance(content, dict):
            data = content
        else:
            data = {'正文': str(content)}
        try:
            params = {
                'title': title,
                'openid': send_openid
            }
            params.update(data)
            resp = requests.get(self.__URL__, params=params)
            if resp.status_code == 200:
                # print(resp.text)
                if '提交成功' in resp.text:
                    return self.return_success
                else:
                    self.return_fail['msg'] = '请求失败'
                    return self.return_fail

            self.return_fail['msg'] = '网络请求失败'
            return self.return_fail
        except Exception as exception:
            self.return_fail['msg'] = str(exception)
            return self.return_fail

