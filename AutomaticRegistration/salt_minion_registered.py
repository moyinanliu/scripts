#!/usr/bin/env python
# encoding:utf-8

""" 自动注册salt-minion """

__author__ = "Cai bird"

import os
import subprocess
import traceback
import yaml
import json
import time
import argparse
import urllib.request
import re


def execute(cmd):
    """
    执行shell命令的函数
    :param cmd: shell命令
    :return:
    """
    try:
        subprocess.call(cmd, shell=True)
    except():
        traceback.print_exc()


def get_public_ip():
    """
    获取公网ip
    :return: ip address
    """
    request = urllib.request.Request("http://txt.go.sohu.com/ip/soip")
    response = urllib.request.urlopen(request)
    result = response.read().decode()
    ip = re.search(r'(\d{1,3}\.){3}\d{1,3}', result).group()
    return ip


def registered(host, port, user, password):
    """
    自动注册
    :param host: IP
    :param port: 端口
    :param user: 用户名
    :param password: 密码
    :return:
    """
    # 构造roster文件的内容
    info = {}
    info.update(
        host=host,
        port=port,
        user=user,
        password=password,
        sudo=True
    )
    roster = {'web1': info}
    # ya = yaml.load(json.dumps(roster), Loader=yaml.FullLoader)
    ya = yaml.load(json.dumps(roster))
    y = yaml.safe_dump(ya, default_flow_style=False)

    # 将内容写入roster
    roster_file = '/etc/salt/%s' % host
    with open(roster_file, 'w') as fw:
        fw.write(y)

    # 调salt-ssh命令安装salt-minion
    execute("yum install -y https://repo.saltstack.com/py3/redhat/salt-py3-repo-2019.2.el7.noarch.rpm ")
    execute("yum install -y salt-minion")

    # 修改minion的配置文件 重启minion
    # 在master端创建好
    src_minion_conf_file = '/srv/salt/base/template_minion_config/template'
    dst_minion_conf_file = '/srv/salt/base/template_minion_config/minion'
    with open(src_minion_conf_file) as fr, open(dst_minion_conf_file, 'w') as fw:
        lines = [line for line in fr.readlines()]
        for line in lines:
            if line.startswith("id"):
                line_ = line.replace('{{host}}', host)
            elif line.startswith("master"):
                line_ = line.replace('{{master}}', get_public_ip())
            line = line_
            fw.write(line)

    # 同步到minion端
    cmd = "salt-ssh --roster-file=%s '*' state.apply file_sync pillar=\"{'src':%s, 'dst':'/etc/salt/minion'}\"" % (
        roster_file, dst_minion_conf_file)
    execute(cmd)

    # 启动
    execute("salt-ssh --roster-file=%s '*' -r 'systemctl restart salt-minion'" % roster_file)
    os.remove(dst_minion_conf_file)
    time.sleep(4)

    # 接受key
    execute('salt-key -a %s -y' % host)


if __name__ == "__main__":

    parse = argparse.ArgumentParser()

    parse.add_argument("-H", "--host", required=True, help="minion的ip地址", metavar='')
    parse.add_argument("-P", "--port", required=True, help="minion的ssh端口", metavar='')
    parse.add_argument("-u", "--user", required=True, help="minion的用户名", metavar='')
    parse.add_argument("-p", "--password", required=True, help="minion的密码", metavar='')

    args = parse.parse_args()

    registered(args.host, args.port, args.user, args.password)
