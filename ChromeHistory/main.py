import os
import getpass
import sqlite3  
import jieba
import jieba.analyse
import sys
import codecs
import time

count=0#总访问网站数（可能不包括刷新）
rawdate=[]#所有记录  0:站点  1：标题  2：访问次数  3：最近访问时间
webs=[]#所有站点及次数   0：站点  1：次数
useday=0#使用的日子
days=[]#所有使用的日子    0：日期    1：打开网站次数
tdaytweb=[]#前几名日子访问的第一名站点    0:日子   1：次数   2：网站   3.关键字
keyword=[]#年度关键字
badwords=['教程','https','com','百度搜','百度','搜索','知道','一下']#网页标题里面可能会出现的垃圾词汇

class wintime:#因为chrome历史记录的时间戳是从1601年开始的微秒数，没找到现成的api，就造了个轮子
    year=1601
    mon=1
    day=1
    mons=[31,28,31,30,31,30,31,31,30,31,30,31]
    mons2=[31,29,31,30,31,30,31,31,30,31,30,31]
    mo=[0,0,0,0,0,0,0,0,0,0,0,0]

    def run(self,y):#是否闰年
        if(y%100==0):
            if(y%400==0):
                return True
        elif(y%4==0):
            return True
        return False

    def yearday(self,y):#一年的天数
        if(self.run(y)):
            return 366
        else:
            return 365

    def addmon(self):
        if(self.mon==12):
            self.mon=1
            self.year+=1
        else:
            self.mon+=1

    def adday(self):
        if(self.run(self.year)):
            self.mo=self.mons2
        else:
            self.mo=self.mons
        if(self.day==self.mo[self.mon-1]):
            self.day=1
            self.addmon()
        else:
            self.day+=1

    def countday(self,ti):
        if(ti==0):
            return 0
        ti//=1000000#秒
        return ti//3600//24#天

    def timeday(self,ti):#精确到天
        if(ti==0):
            return[0,0,0]
        ti=self.countday(ti)
        while(ti>=self.yearday(self.year)):
            ti-=self.yearday(self.year)
            self.year+=1
        if(self.run(self.year)):
            self.mo=self.mons2
        else:
            self.mo=self.mons
        while(ti>=self.mo[self.mon-1]):
            ti-=self.mo[self.mon-1]
            self.addmon()
        self.day=ti
        self.adday()
        
        return[self.year,self.mon,self.day]


#使用 结巴api，得到高频词汇
#输入输出：字符串列表
def keywords(s):
    global badwords
    for i in badwords:
        jieba.del_word(i)#屏蔽垃圾词汇
    return jieba.analyse.extract_tags(" ".join(s), topK=20, withWeight=False, allowPOS=())


#对网址经行裁剪，只留主域名，方便统计
def mainweb(url):
    try:  
        parsed_url_components = url.split('//')  
        sublevel_split = parsed_url_components[1].split('/', 1)  
        if(url[:4]=="http"):
            domain =sublevel_split[0].split('.')  
            return domain[len(domain)-2]+"."+domain[len(domain)-1]
        else:
            if(parsed_url_components[1][0]=="/"):
                return sublevel_split[1].split('/', 1)[0]#file:///
            else:
                return sublevel_split[0]#ftp://
    except IndexError:  
        print('URL format error!') 


#从chrome历史记录路径读取数据，使用sqlite3打开
def readsql():
    global count,rawdate,useday
    dbpath=os.path.join('C:/Users/'+getpass.getuser()+'/AppData/Local/Google/Chrome/User Data/Default', 'History')
    if(os.path.exists(dbpath)==False):
        dbpath=os.path.join('C:/Users/'+getpass.getuser()+'/AppData/Local/Google/Chrome/User Data/Default', 'history')
        if(os.path.exists(dbpath)==False):
            print("路径出错，请确保系统是win7+，且安装了chrome")
            return
    c = sqlite3.connect(dbpath)  
    cursor = c.cursor()  
    cursor.execute("SELECT urls.url, title, urls.visit_count, urls.last_visit_time FROM urls WHERE urls.last_visit_time>0 ORDER BY last_visit_time ;") 
    results = cursor.fetchall()
    c.close()
    count=len(results)#所有有记录数
    startday=results[0][3]#第一条记录的时间
    endday=results[count-1][3]#最后一条记录的时间
    for i in results:
        t=wintime()#将每条记录加入rawdate里。（我知道我拼错了）
        rawdate.append([mainweb(i[0]),i[1],i[2],t.timeday(i[3])])
    t=wintime()
    useday=t.countday(endday-startday)#使用时长


#统计，排序得到前几名网站和前几名日期
def tops():
    global rawdate,webs,days,tdaytweb
    for i in rawdate:
        exw=False#该站点是否已有记录
        exd=False#该日子是否已有记录
        for j in webs:
            if(i[0]==j[0]):
                exw=True
                j[1]+=i[2]
        for j in days:
            if(i[3]==j[0]):
                exd=True
                j[1]+=i[2]
        if(exw==False):
            webs.append([i[0],i[2]])   
        if(exd==False):
            days.append([i[3],i[2]])
    webs.sort(key=lambda a:a[1],reverse=True)#按访问次数从大到小排序
    days.sort(key=lambda a:a[1],reverse=True)
    #在rawdate里找前10名日子浏览的网页，并排名，记录在tdaytweb
    topdays=days[:10]
    for j in topdays:#topdays   [0：日期    1：打开网站次数] ……
        s=[]
        topweb=[]#  0：网站   1：次数
        for i in rawdate:#  0:站点  1：标题  2：访问次数  3：最近访问时间
            if(i[3]==j[0]):#rawdate中该记录属于前几名日子
                s.append(i[1])
                ex=False
                for z in topweb:
                    if(z[0]==i[0]):
                        ex=True
                        z[1]+=i[2]
                if(ex==False):
                    topweb.append([i[0],i[2]])
        topweb.sort(key=lambda a:a[1],reverse=True)
        tdaytweb.append([j[0],j[1],topweb[:3],keywords(s)[:3]])#0:日子   1：次数   2：网站
    days=[]
    webs=webs[:10]


#调用结巴，得到年度关键词组
def word():
    global rawdate,keyword
    title=[]
    for i in rawdate:
        title.append(i[1])
    keyword=keywords(title)


#写出到当前目录下的markdown文件
def out():
    global count,rawdate,useday,keyword,webs,days,tdaytweb
    fp=codecs.open(os.path.join(sys.path[0],"我和Chrome一同留下的记录.md"),'w+',"utf-8")

    s=["# 我和Chrome一同留下的记录\n"]
    s.append("\n## 在过去的 *"+str(useday)+"* 天内，我使用Chrome打开了 *"+str(count)+"* 个网页。\n")
    s.append("\n## 我是这几个站点的常客：\n\n")
    i=0
    while(i<10):
        s.append("1. ["+webs[i][0]+"](http://"+webs[i][0]+") :我共访问了 **"+str(webs[i][1])+"** 次\n")
        i+=1
    s.append("\n## 这几天不平凡：\n")
    i=0
    while(i<6):
        m=tdaytweb[i]
        date=str(m[0][0])+"年"+str(m[0][1])+"月"+str(m[0][2])+"日"
        s.append("\n* 在 *"+date+"* ,我访问了：\n")
        for j in m[2]:
            s.append("  * **" +str(j[1])+"** 次 ["+j[0]+"](http://"+j[0]+")\n")
        s.append("\n  这一天的关键词是： *"+"* , *".join(m[3])+"*\n")
        i+=1
    s.append("\n## 属于我的词组是：\n\n```txt\n")
    i=0
    while(i<4):
        s.append("     ".join(keyword[i*5:i*5+5])+"\n")
        i+=1
    s.append("```\n")
    s.append("\n<p align=\"right\">"+time.strftime('%Y-%m-%d',time.localtime(time.time()))+"</p>\n")
    for i in s:
        fp.seek(0,2)
        fp.write(i)
    fp.close()

#执行
readsql()
tops()
word()
out()
            
