#!/usr/bin/python
#-*- coding:utf-8 -*-
#Guard.py
#name方法依赖系统的ps 和grep不过。。。估计所有系统都装有吧
import os,sys,commands,time
import ConfigParser
import subprocess

def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def qupid():
    f = None
    line = None
    ff = None
    conf = './Guard.conf'#配置文件路径
    if os.path.exists(conf)==True:#判断配置文件是否存在
          cf = ConfigParser.ConfigParser()
          cf.read(conf)

          db_pid = cf.get("setting", "pid")#读取配置中的pid文件路径
          db_name = cf.get("setting", "name")#读取配置中的pid文件路径
          #cf.set("baseconf", "db_pass", "123456")
          #cf.write(open("config_file_path", "w"))
    else:
          db_pid = ""
    pid = str(db_pid)#到文本
    print pid
    if os.path.exists(pid)==True:#pid文件路径是否存在
        f = open(pid,'r')
        for line in f.readlines()[:1]:
            ff = line.find("\n")
            line = line[:ff]
            f.close()
        if int(line)>0:
            print GetNowTime() + " PID_进程已存在，启动守护进程。"
            Guard_pid()
        else:
            print "进程不存在"
            exit()
    elif str(db_name)!="":
        print GetNowTime() + " NAME_启动守护进程。"
        Guard_name()
    else:
        print "PID文件/进程名不存在"
        exit()

def Guard_name():
    conf = './Guard.conf'
    if os.path.exists(conf)==True:#判断配置文件是否存在
          cf = ConfigParser.ConfigParser()
          cf.read(conf)
          
          db_method = cf.get("setting", "method")#读取配置中的shell执行方法 commands/os/subprocess 默认commands
          db_name = cf.get("setting", "name")#读取配置中的pid文件路径
          db_cd = cf.get("setting", "cd")#读取配置中的cd的目标目录默认/root/
          db_shell = cf.get("setting", "shell")#读取配置中的需要守护的程序的启动方法
          db_sleep = cf.get("setting", "sleep")#读取配置中的检测延迟
          #cf.set("baseconf", "db_pass", "123456")
          #cf.write(open("config_file_path", "w"))
    name_ = str(db_name)
    #---------------
    cd = str(db_cd)#到文本 挂载目录
    if cd == "":
        cd='/root/'
    elif os.path.exists(cd)==False:
        cd='/root/'
    #---------------
    shell = str(db_shell)#到文本 程序启动方法
    #---------------
    shell_method = str(db_method)
    if shell_method != "subprocess" and shell_method != "os":
        shell_method == "commands"
    #---------------
    cx_shell = 'ps -ef | grep '+name_+' | grep -v grep'
    
    if shell_method == "subprocess":
        sb = subprocess.Popen(cx_shell,shell=True)
        sb = sb.communicate()
    elif shell_method == "commands":
        sb = commands.getstatusoutput(cx_shell)
    else:
        sb = os.system(cx_shell)
    sb_ = str(sb)
    #<subprocess.Popen object at 0x7f6ea5935310>
    #commands如果没有结果他会返回(256, '')
    #os空白会返回256
    if sb_ == "(256, \'\')" and  shell_method == "commands":
        print '与进程名匹配的进程不存在'
        exit()
    elif sb_.startswith("<subprocess.Popen object at 0x"):
        print '与进程名匹配的进程不存在'
        exit()
    elif sb_ == "256" and shell_method == "os":
        print '与进程名匹配的进程不存在'
        exit()
    else:
        print '进程名存在开启守护'
    yc = int(db_sleep)
    while 1:
        if shell_method == "subprocess":
            sb = subprocess.Popen(cx_shell,shell=True)
            sb.communicate()
        elif shell_method == "commands":
            sb = commands.getstatusoutput(cx_shell)
        else:
            sb = os.system(cx_shell)
        sb_ = str(sb)
        if sb_ == "(256, \'\')" and  shell_method == "commands":
            jieguo = "no"
        elif sb_.startswith("<subprocess.Popen object at 0x"):
            jieguo = "no"
        elif sb_ == "256" and shell_method == "os":
            jieguo = "no"
        else:
            jieguo = "yes"
        if jieguo == "no":
            #进程不存在
            print str(GetNowTime()) + " 进程不存在尝试启动_name"
            if shell_method=="commands":
                commands.getstatusoutput('cd ' + cd)
                commands_ = commands.getstatusoutput(shell)
                print GetNowTime() +" "+ str(commands_)
            elif shell_method=="os":
                os.system('cd ' + cd)
                os_ = os.system(shell)
                print GetNowTime() +" "+ str(os_)
            else:
                subprocess.Popen('cd ' + cd,shell=True)
                subprocess_ = subprocess.Popen(shell,shell=True)
                subprocess_.communicate()
                print GetNowTime() +" "+ str(subprocess_)
            time.sleep(yc)
        else:
            time.sleep(yc)



def Guard_pid():
    conf = './Guard.conf'
    if os.path.exists(conf)==True:#判断配置文件是否存在
          cf = ConfigParser.ConfigParser()
          cf.read(conf)
          
          db_method = cf.get("setting", "method")#读取配置中的shell执行方法 commands/os/subprocess 默认commands
          db_pid = cf.get("setting", "pid")#读取配置中的pid文件路径
          db_cd = cf.get("setting", "cd")#读取配置中的cd的目标目录默认/root/
          db_shell = cf.get("setting", "shell")#读取配置中的需要守护的程序的启动方法
          db_sleep = cf.get("setting", "sleep")#读取配置中的检测延迟
          #cf.set("baseconf", "db_pass", "123456")
          #cf.write(open("config_file_path", "w"))
    else:
          db_pid = ""
    pid = str(db_pid)#到文本 pid文件路径
    #---------------
    cd = str(db_cd)#到文本 挂载目录
    if cd == "":
        cd='/root/'
    elif os.path.exists(cd)==False:
        cd='/root/'
    #---------------
    shell = str(db_shell)#到文本 程序启动方法
    #---------------
    shell_method = str(db_method)
    if shell_method != "os" and shell_method != "subprocess":
        shell_method == "commands"
    #---------------
    yc = int(db_sleep)
    while 1:
        if os.path.exists(pid)==True:
            f = open(pid,'r')
            for line in f.readlines()[:1]:
                ff = line.find("\n")
                line = line[:ff]
                f.close()
        else:
            line = "0"
        if int(line)==0 or int(line)<0:
            #进程不存在
            print str(GetNowTime()) + " 进程不存在尝试启动_pid"
            if shell_method=="commands":
                commands.getstatusoutput('cd ' + cd)
                commands_ = commands.getstatusoutput(shell)
                print GetNowTime() +" "+ str(commands_)
            elif shell_method=="os":
                os.system('cd ' + cd)
                os_ = os.system(shell)
                print GetNowTime() +" "+ str(os_)
            else:
                subprocess.Popen('cd ' + cd,shell=True)
                subprocess_ = subprocess.Popen(shell,shell=True)
                subprocess_.communicate()
                print GetNowTime() +" "+ str(subprocess_)
            time.sleep(yc)
        else:
            time.sleep(yc)
def main():
    qupid()

if __name__ == "__main__":
    main()
