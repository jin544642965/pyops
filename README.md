

# pyops
运维自动化平台

环境准备:
1.MYSQL



demo
http://demo-pyops.fskangda.com:8001(停用)
账号：demo 密码：demo@demo

每20分钟重置一次数据


注意修改lib/common.py的token
cmdb/cmdb_agent.py的token

汇集常用功能：
cmdb、wiki、网盘、用户管理

python3环境安装
yum install python-pip
pip install --upgrade pip
pip install virtualenv

安装
mkdir /opt/py_env
cd /opt/py_env
virtualenv --python=python3.6 pyops

source /opt/py_env/pyops/bin/activate

进入项目目录安装依赖包
cd /opt/pyops
pip install -r requirements.txt


