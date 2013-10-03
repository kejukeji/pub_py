# coding: utf-8

"""
    开发人员各自的配置数据
"""

# 配置文件路径，测试服务器和生产服务器载入不同的配置文件
CONFIG_FILE = 'setting/lyw.cfg'  # 吕义旺的配置文件
#CONFIG_FILE = 'setting/xj.cfg'  # 向进的配置文件
#CONFIG_FILE = 'setting/server.cfg'  # 生产服务器配置文件

# 连接数据库的变量，这个本来是在配置文件那里的，但是有一个文件包含的问题
# 连接 生产服务器
#SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/bar?charset=utf8'
# 连接 公司的测试服务器
# 连接 吕义旺自己的本地服务器
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3306/bar?charset=utf8'