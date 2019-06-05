#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponse
try:
    import configparser as cp
except Exception as msg:
    print(msg)
    import ConfigParser as cp
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


def get_dir(args):
    config = cp.RawConfigParser()
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(dirs+'/adminset.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        a_path = config.get('config', 'ansible_path')
        r_path = config.get('config', 'roles_path')
        p_path = config.get('config', 'playbook_path')
        s_path = config.get('config', 'scripts_path')
        token = config.get('token', 'token')
        ssh_pwd = config.get('token', 'ssh_pwd')
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')
        mongodb_ip = config.get('mongodb', 'mongodb_ip')
        mongodb_port = config.get('mongodb', 'mongodb_port')
        mongodb_user = config.get('mongodb', 'mongodb_user')
        mongodb_pwd = config.get('mongodb', 'mongodb_pwd')
        mongodb_collection = config.get('mongodb', 'collection')
        webssh_domain = config.get('webssh', 'domain')
        redis_host = config.get('redis', 'redis_host')
        redis_port = config.get('redis', 'redis_port')
        redis_password = config.get('redis', 'redis_password')
        redis_db = config.get('redis', 'redis_db')
        ldap_enable = config.get('ldap', 'ldap_enable')
        ldap_server = config.get('ldap', 'ldap_server')
        ldap_port = config.get('ldap', 'ldap_port')
        base_dn = config.get('ldap', 'base_dn')
        ldap_manager = config.get('ldap', 'ldap_manager')
        ldap_password = config.get('ldap', 'ldap_password')
        ldap_filter = config.get('ldap', 'ldap_filter')
        require_group = config.get('ldap', 'require_group')
        nickname = config.get('ldap', 'nickname')
        is_active = config.get('ldap', 'is_active')
        is_superuser = config.get('ldap', 'is_superuser')
    # 根据传入参数返回变量以获取配置，返回变量名与参数名相同
    if args:
        return vars()[args]
    else:
        return HttpResponse(status=403)


@login_required()
def get_token(request):
    if request.method == 'POST':
        new_token = get_user_model().objects.make_random_password(length=12, allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
        return HttpResponse(new_token)
    else:
        return True
