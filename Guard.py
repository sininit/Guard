#!/usr/bin/python
#-*- coding:utf-8 -*-
#Guard.py
#源码作者784920843转载修改请不要去掉版权谢谢。
#name方法依赖系统的ps 和grep不过。。。估计所有系统都装有吧
import os,sys,time
import ConfigParser
import subprocess

def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def go():
    conf = './Guard.conf'#配置文件路径
    if os.path.exists(conf)==True:#判断配置文件是否存在
          cf = ConfigParser.ConfigParser()
          cf.read(conf)

          db_pid = cf.get("setting", "pid")#读取配置中的pid文件路径
          db_name = cf.get("setting", "name")#读取配置中的pid文件路径
          db_name_vague = cf.get("setting", "name_vague")
          
          #cf.set("baseconf", "db_pass", "123456")
          #cf.write(open("config_file_path", "w"))
    else:
          db_pid = ""
    if pid_if(db_pid) != 0:
        print GetNowTime() + " PID_进程已存在，启动守护进程。"
        Guard_pid()
    elif db_name != "" and os.path.exists(db_pid)==False and db_pid == "":
        if name_if(db_name,db_name_vague) == "yes":
            print GetNowTime() + " NAME_启动守护进程。"
            Guard_name()
        else:
            print '与进程名匹配的进程不存在'
            exit()
    else:
        print "PID文件/进程名不存在"
        exit()
        
def pid_if(pid):
    line = None
    if os.path.exists(pid)==True:#pid文件路径是否存在
        f = open(pid,'r')
        for line in f.readlines()[:1]:
            ff = line.find("\n")
            line = line[:ff]
            f.close()
    else:
        line = "0"
    if int(line)==0 or int(line)<0:
        line = "0"
    back = int(line)
    return (back)
    
def name_if(name,name_vague):
    sb = None
    sb_ = None
    #---------------
    if name_vague =="on":
        cx_shell = 'ps -ef | grep ' + name + ' | grep -v grep'
    else:
        cx_shell = 'ps -ef | grep -w ' + name + ' | grep -v grep'
        
    sb = subprocess.call(cx_shell,shell=True)
    sb_ = str(sb)
    if sb_ == "0":
        jieguo = "yes"
    else:
        jieguo = "no"
    print jieguo
    return (jieguo)
    
def Guard_name():
    conf = './Guard.conf'
    if os.path.exists(conf)==True:#判断配置文件是否存在
          cf = ConfigParser.ConfigParser()
          cf.read(conf)
          
          db_name_vague = cf.get("setting", "name_vague")
          db_name = cf.get("setting", "name")#读取配置中的pid文件路径
          db_cd = cf.get("setting", "cd")#读取配置中的cd的目标目录默认/root/
          db_shell = cf.get("setting", "shell")#读取配置中的需要守护的程序的启动方法
          db_shell_down = cf.get("setting", "shell_down")#读取配置中的需要守护的程序的关闭方法
          db_sleep = cf.get("setting", "sleep")#读取配置中的检测延迟
          #cf.set("baseconf", "db_pass", "123456")
          #cf.write(open("config_file_path", "w"))
    #---------------
    if db_cd == "":
        db_cd='/root/'
    elif os.path.exists(db_cd)==False:
        db_cd='/root/'
    #---------------
    yc = int(db_sleep)
    while 1:
        time.sleep(yc)
        jieguo = name_if(db_name,db_name_vague)
        if jieguo == "no":
            #进程不存在
            if db_shell_down !="":
                subprocess_ = subprocess.call(db_shell_down,shell=True,cwd=db_cd)
            print str(GetNowTime()) + " 进程不存在尝试启动_name"
            subprocess_ = subprocess.call(db_shell,shell=True,cwd=db_cd)
            print GetNowTime() +" "+ str(subprocess_)
            
            
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
          db_shell_down = cf.get("setting", "shell_down")#读取配置中的需要守护的程序的关闭方法
          #cf.set("baseconf", "db_pass", "123456") 
          #cf.write(open("config_file_path", "w"))
    else:
          db_pid = ""
    #---------------
    if db_cd == "":
        db_cd='/root/'
    elif os.path.exists(db_cd)==False:
        db_cd='/root/'
    #---------------
    yc = int(db_sleep)
    while 1:
        time.sleep(yc)
        if pid_if(db_pid) == 0:
            #进程不存在
            if db_shell_down !="":
                subprocess_ = subprocess.call(db_shell_down,shell=True,cwd=db_cd)
            print str(GetNowTime()) + " 进程不存在尝试启动_pid"
            subprocess_ = subprocess.call(db_shell,shell=True,cwd=db_cd)
            print GetNowTime() +" "+ str(subprocess_)
            
def main():
    go()

if __name__ == "__main__":
    main()
