#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 此脚本已在CentOS 7上测试通过
# 作者：H&C

import os
import time

def ssh_keygen():
    '''
    这是一个实现面交互创建SSH密钥对的函数
    :return:返回面交互创建密钥对的执行结果
    '''
    #删除原有SSH密钥对信息
    os.system('rm -rf /root/.ssh/id_dsa*')
    time.sleep(1)
    #免交互创建密钥对
    res = os.system('ssh-keygen -t dsa -f "/root/.ssh/id_dsa" -N ""')
    time.sleep(1)

    return res


def distribute_key():
    '''
    这是一个SSH批量分发公钥的函数
    :return:
    '''
    #安装sshpass
    os.system('yum install -y sshpass')
    time.sleep(1)
    #定义一个os_passdord变量，用于存放受控端系统密码
    os_password = 'bd@bdht.C0M'
    #定义一个ip_list变量，用于存放受控端IP地址
    ip_list = ['192.168.50.148',]

    for i in ip_list:
        #SSH批量分发公钥
        #-p：指定ssh连接用户密码
        #-o：StrictHostKeyChecking=no 避免第一次登录出现公钥检查
        os.system('sshpass -p{} ssh-copy-id -i /root/.ssh/id_dsa.pub "-o StrictHostKeyChecking=no" root@{}'.format(os_password,i))
        time.sleep(1)
        #为受控机安装libselinx-python，让Python程序顺利通过selinux
        print('=' * 50)
        os.system('ssh {} yum install -y libselinx-python'.format(i))
        print('=' * 50)
        time.sleep(1)

if __name__ == '__main__':
    #判断创建SSH密钥对是否成功，如果不成功，再次执行
    if ssh_keygen() == 1:
        print('=' * 30)
        print("创建SSH密钥对失败！将尝试重新创建……")
        print('=' * 30)
        time.sleep(1)
        ssh_keygen()
    #如果成功，则输出成功信息
    else:
        print('=' * 30)
        print("创建SSH密钥对成功！")
        print('=' * 30)
        time.sleep(1)

    distribute_key()
