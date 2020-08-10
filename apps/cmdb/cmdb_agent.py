#!/usr/bin/python2.7
# _*_coding:utf-8 _*_
import logging
import os
import socket
import platform
import json
import urllib2



"""
description: 客户端采用linux自带python2.7

"""

VERSION = '0.1.0'

app_token = "AT_ZnmHbwWYzrxjIEyQni4miU72dcLy43WW"

# 获取当前脚本的目录
pwd_dir = os.path.dirname(os.path.abspath(__file__))

# cmdb server url

server_url = 'http://pyops.ehuzhu.com/cmdb/api'

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s [%(levelname)s] %(message)s',
#                     filename=os.path.join(pwd_dir, 'cmdb_agent.log'),
#                     filemode='a')


class HostReport(object):
    def __init__(self):
        # 初始化一个采集器
        collector = LinuxCollector()
        self.host = collector.collect()
        # 查询主机api
        self.search_url = '{0}/host_search'.format(server_url)
        # format可以直接格式化元组、列表、字典，更灵活
        self.post_url = '{0}/host'.format(server_url)

    def update_host(self, intranet_ip, host):
        update_url = self.post_url + '/update/' + intranet_ip

        data = {
            'token' : app_token,
            'host':  self.host
        }
        res = urllib2.urlopen(update_url, data=json.dumps(data))
        if res.getcode() != 200:
            raise Exception(res.read())
        return res.read()

    def get_host_intranet_ip(self):
        data = {
            'token' : app_token,
            'intranet_ip': self.host['intranet_ip']
        }
        res = urllib2.urlopen(self.search_url, data=json.dumps(data))
        res_dict = json.loads(res.read())

        if res_dict['code'] == 200:
            return res_dict['host']['intranet_ip']

        return None

    def create_host(self):

        data = {
            'token': app_token,
            'host': self.host
        }
        host_add_url = self.post_url + '/add'

        res = urllib2.urlopen(host_add_url, data=json.dumps(data))

        if res.getcode() != 200:
            raise Exception(res.read())

        return res.read()

    def report(self):
        host = self.host

        # 从数据中查看IP是否存在
        intranet_ip = self.get_host_intranet_ip()

        if intranet_ip is None:
            logging.warning('host is not register in cmdb server ,create it')
            return self.create_host()

        return self.update_host(intranet_ip, host)

class LinuxCollector(object):
    def collect(self):
        """
        :return dict:
        """
        return {
            'cpu_model': self._collect_cpu_model(),
            'cpu_num':self._collect_cpu_num(),
            'memory': self._collect_memory(),
            'disk': self._collect_disk(),
            'intranet_ip': self._collect_intranet_ip(),
            'internet_ip': self._collect_internet_ip(),
            'hostname': socket.gethostname(),
            'os': platform.platform(),
            'idc_id': 1,
        }

    # 收集cpu型号
    @staticmethod
    def _collect_cpu_model():
        cpu_model = os.popen("awk -F: '/model name/{print $2}' /proc/cpuinfo|uniq").read().rstrip()
        return cpu_model

    # 采集cpu个数
    def _collect_cpu_num(self):
        cpu_num = os.popen("cat /proc/cpuinfo|grep 'cpu core'|uniq|awk '{print $4}'").read().rstrip()
        return cpu_num

    @staticmethod
    def _collect_memory():
        # 内存个数
        mems = int(os.popen("dmidecode -t memory |grep Size:|wc -l").read())
        mem_size = int(os.popen("dmidecode -t memory |grep Size:|awk '{print $2}'|uniq").read())
        mem_total = mems * mem_size / 1024
        return '{0} GB'.format(mem_total)

    @staticmethod
    def _collect_disk():
        disk = os.popen("df -h|awk '/dev\/vd/ {print $1,$2}'").read().rstrip()
        return disk

    # 采集内网IP
    def _collect_intranet_ip(self):
        intranet_ip = os.popen("ip addr |grep inet |grep -v inet6 |grep eth0|awk '{print $2}'|awk -F '/' '{print $1}'").read().rstrip()
        return intranet_ip

    # 采集外网ip
    def _collect_internet_ip(self):
        internet_ip = os.popen("curl tnx.nl/ip").read().rstrip()
        return internet_ip


if __name__ == '__main__':
    res = HostReport().report()
    #logging.info(json.dumps(res))

