#!/usr/bin/python
#-*- coding:utf-8 -*-
#Guard.py
#源码作者784920843转载修改请不要去掉版权谢谢。
#name方法依赖系统的ps 和grep不过。。。估计所有系统都装有吧
import os,sys,commands,time
import ConfigParser
import subprocess

def GetNowTime():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def qupid():
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
          
          db_name_vague = cf.get("setting", "name_vague")
          
          db_method = cf.get("setting", "method")#读取配置中的shell执行方法 commands/os/subprocess 默认commands
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
    if db_method != "subprocess" and db_method != "os":
        db_method == "commands"
    #---------------
    if db_name_vague =="on":
        cx_shell = 'ps -ef | grep ' + db_name + ' | grep -v grep'
    else:
        cx_shell = 'ps -ef | grep -w ' + db_name + ' | grep -v grep'
    if db_method == "subprocess":
        sb = subprocess.call(cx_shell,shell=True)
    elif db_method == "commands":
        sb = commands.getstatusoutput(cx_shell)
    else:
        sb = os.system(cx_shell)
    sb_ = str(sb)
    #subprocess成功反回0
    #commands如果没有结果他会返回(256, '')
    #os空白会返回256
    if db_method == "commands":
        if sb_ == "(256, \'\')":
            print '与进程名匹配的进程不存在'
            exit()
    elif db_method == "subprocess":
        if sb_ != "0":
            print '与进程名匹配的进程不存在'
            exit()
    elif db_method == "os":
        if sb_ == "256":
            print '与进程名匹配的进程不存在'
            exit()
    print '进程名存在开启守护'
    yc = int(db_sleep)
    while 1:
        sb = None
        sb_ = None
        time.sleep(yc)
        if db_method == "subprocess":
            sb = subprocess.call(cx_shell,shell=True)
        elif db_method == "commands":
            sb = commands.getstatusoutput(cx_shell)
        else:
            sb = os.system(cx_shell)
        sb_ = str(sb)
        if db_method == "commands":
            if sb_ == "(256, \'\')":
                jieguo = "no"
            else:
                jieguo = "yes"
        elif db_method == "subprocess":
            if sb_ != "0":
                jieguo = "no"
            else:
                jieguo = "yes"
        elif db_method == "os":
            if sb_ == "256":
                jieguo = "no"
            else:
                jieguo = "yes"
        if jieguo == "no":
            #进程不存在
            if db_shell_down !="":
                if db_method=="commands":
                    commands_ = commands.getstatusoutput(db_shell_down)
                   
                elif db_method=="os":
                    os_ = os.system(db_shell_down)
                else:
                    subprocess_ = subprocess.call(db_shell_down,shell=True)
            
            print str(GetNowTime()) + " 进程不存在尝试启动_name"
            if db_method=="commands":
                commands_ = commands.getstatusoutput('cd ' + db_cd +" && "+ db_shell)
                print GetNowTime() +" "+ str(commands_)
            elif db_method=="os":
                os_ = os.system('cd ' + db_cd +" && "+ db_shell)
                print GetNowTime() +" "+ str(os_)
            else:
                subprocess_ = subprocess.call('cd ' + db_cd +" && "+ db_shell,shell=True)
                print GetNowTime() +" "+ str(subprocess_)
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
    if db_method != "os" and db_method != "subprocess":
        db_method == "commands"
    #---------------
    yc = int(db_sleep)
    while 1:
        line = None
        time.sleep(yc)
        if os.path.exists(db_pid)==True:
            f = open(db_pid,'r')
            for line in f.readlines()[:1]:
                ff = line.find("\n")
                line = line[:ff]
                f.close()
        else:
            line = "0"
        if int(line)==0 or int(line)<0:
            #进程不存在
            if db_shell_down !="":
                if db_method=="commands":
                    commands_ = commands.getstatusoutput(db_shell_down)
                   
                elif db_method=="os":
                    os_ = os.system(db_shell_down)
                else:
                    subprocess_ = subprocess.call(db_shell_down,shell=True)
            print str(GetNowTime()) + " 进程不存在尝试启动_pid"
            if db_method=="commands":
                commands_ = commands.getstatusoutput('cd ' + db_cd +" && "+ db_shell)
                print GetNowTime() +" "+ str(commands_)
            elif db_method=="os":
                os_ = os.system('cd ' + db_cd +" && "+ db_shell)
                print GetNowTime() +" "+ str(os_)
            else:
                subprocess_ = subprocess.call('cd ' + db_cd +" && "+ db_shell,shell=True)
                print GetNowTime() +" "+ str(subprocess_)
            time.sleep(yc)
def main():
    qupid()

if __name__ == "__main__":
    main()
