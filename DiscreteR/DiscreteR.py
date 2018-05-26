import matplotlib.pyplot as plt
from math import pi
from numpy import cos, sin
def readMatrix():
    '''读入关系的矩阵形式'''
    re=[]
    l=int(input("请输入矩阵行数行数："))
    print("请输入矩阵：")
    for i in range(l):
        t=[]
        s=input()
        for j in range(l):
            if(int(s[j])!=0):
                t.append(True)
            else:
                t.append(False)
        re.append(t)
        #a.append(list(input()))#一句就行，但得到的是char，，不好
    return re

def frame(a):
    '''输出一个a*a的全0的矩阵'''
    re=[]
    for i in range(a):#画出矩阵框架
        t=[]
        for j in range(a):
            t.append(False)
        re.append(t)
    return re

def readSet():
    '''读取关系的集合形式'''
    print("请输入集合：格式：比如集合{<1,2>,<3,4>}请输入 <1,2>,<3,4>")
    l=input().replace(" ","")
    l=l.split(">,<")
    l[0]=l[0][1:len(l[0])]   
    l[len(l)-1]=l[len(l)-1][0:(len(l[len(l)-1])-1)]
    m=[]
    for i in l:
        n=i.split(",")
        for j in range(len(n)):
            n[j]=int(n[j])
        m.append(n)
    max=m[0][0]#求出矩阵的边长
    for i in m:
        for j in i:
            if(j>max):
                max=j
    re=frame(max)
    for i in m:#填充数据
        re[i[0]-1][i[1]-1]=True
    return re#

def stringMatrix(k):
    '''将m格式化成矩阵的字符串形式'''
    re=""
    for i in k:
        for j in i:
            if(j):
                re+="1 "
            else:
                re+="0 "
        re+="\n"
    return re

def showMatrix(k):
    '''展示关系的矩阵'''
    print(stringMatrix(k))

def stringSet(m):
    '''将m格式化成集合的字符串形式'''
    re=""
    count=0
    for i in range(len(m)):
        for j in range(len(m)):
            if(m[i][j]):
                count+=1
    for i in range(len(m)):
        for j in range(len(m)):
            if(m[i][j]):
                re=re+"<"+str(i+1)+","+str(j+1)+">"
                count-=1
                if(count>0):
                    re=re+","
    return re

def showSet(m):
    '''以集合的形式展示m '''
    print(stringSet(m))

def inverse(m):
    '''转置'''
    n=[]
    for i in range(len(m[0])):
        t=[]
        for j in range(len(m[0])):
            t.append(m[j][i])
        n.append(t)
    return n

def multi(n,m):
    '''n乘m，或者n复合m
    此处仅限nm是俩等边长的正方形
    '''
    re=[]
    l=len(n)
    m=inverse(m)
    for i in range(l):
        t=[]
        for j in range(l):
            s=0
            for k in range(l):
                #s+=n[i][k]*m[j][k]#这是算术做法
                s=s or (n[i][k] and m[j][k])#离散数学只需要bool
            t.append(s)
        re.append(t)
    return re

def draw(m):
    '''
    画出关系图
    '''
    com=[]#命令list
    for i in range(len(m)):
        for j in range(len(m)):
            if(m[i][j]):#找到条路径需要画，下面生成命令
                if(i<j):#主对角线之上，方向向右
                    com.append([i+1,j+1,1])
                elif(i==j):#主对角线中，是一个圆
                    com.append([i+1,j+1,0])
                else: #主对角线之下 ，方向左
                    com.append([i+1,j+1,-1])
    #执行命令，画路径
    for i in com:        
        if(i[2]==1):#x轴上，向右，蓝色
            angles_circle = [i*pi/180 for i in range(0,180)] #角度
            color='b'
            x=cos(angles_circle)*(i[1]-i[0])+(i[1]+i[0])#伸缩值+偏移量
            y=sin(angles_circle)*(i[1]-i[0])
        elif(i[2]==-1):#x轴上，向左，绿色
            angles_circle = [i*pi/180 for i in range(180,360)] 
            color='g'
            x=cos(angles_circle)*(i[0]-i[1])+(i[0]+i[1])
            y=sin(angles_circle)*(i[0]-i[1])
        else:#x轴上点，一圈，黄色
            angles_circle = [i*pi/180 for i in range(0,360)] 
            color='y'
            x=cos(angles_circle)/4+i[0]*2-0.25
            y=sin(angles_circle)/4
        plt.plot(x, y,color)
    px=[]#画点x
    py=[]#画点y
    for i in range(1,len(m)+1):
        px.append(2*i)
        py.append(0)
        plt.text(2*i,-0.25,str(i))#坐标轴字
    plt.plot([2,2*len(m)],[0,0],"gray",linewidth=0.5)#X轴
    plt.plot(px, py, 'ro')
    plt.text(0,len(m)*-0.5,"PathDirection:\nblue-->right\ngreen<--left\n")#标注方向
    plt.text(0,len(m)*0.3,"Set:\n{"+stringSet(m)+"}\n"+"Matrix:\n"+stringMatrix(m)+"\n")#标注集合
    plt.axis('equal')#坐标系等值伸缩
    plt.axis('scaled')
    plt.axis('off')#隐藏坐标系
    plt.show()

def jiao(n,m):
    '''求交集'''
    if(len(n)<len(m)):#令n最大
        t=n
        n=m
        m=t
    for i in range(len(m)):
        for j in range(len(m)):
            n[i][j]=n[i][j] and m[i][j]
    return n

def bing(n,m):
    '''并集'''
    if(len(n)<len(m)):#令n最大
        t=n
        n=m
        m=t
    for i in range(len(m)):
        for j in range(len(m)):
            n[i][j]=n[i][j] or m[i][j]
    return n

def I(a):
    '''恒等关系
    a是一个数字
    输出a*a的矩阵'''
    re=frame(a)
    for i in range(a):
        re[i][i]=True
    return re

def E(a):
    '''全域关系
    a是一个数字
    输出a*a的矩阵'''
    re=[]
    for i in range(a):#画出矩阵框架
        t=[]
        for j in range(a):
            t.append(True)
        re.append(t)
    return re

def L(a):
    '''小于等于关系
    a是一个数字
    输出a*a的矩阵'''
    re=frame(a)
    for i in range(a):
        for j in range(a):
            if(i<=j):
                re[i][j]=True

def D(a):
    '''整除关系
    a是一个数字
    输出a*a的矩阵'''
    re=frame(a)
    for i in range(a):
        for j in range(a):
            if(j%i==0):
                re[i][j]=True

def ifInlude(n,m):
    '''n是否是m的子集'''
    if(len(n)>len(m)):
        return False
    for i in range(len(n)):
        for j in range(len(n)):
            if(n[i][j]):
                if(not m[i][j]):
                    return False
    return True

def zifan(m):
    '''m是否有自反性'''
    return ifInlude(I(len(m)),m)

def fanzifan(m):
    '''m是否有反自反性'''
    for i in range(len(n)):
        if(m[i][i]):
            return False
    return True

def duichen(m):
    '''m是否有对称性'''
    for i in range(len(m)):
        for j in range(i):
            if(m[i][j]!=m[j][i]):
                return False
    return True

def fanduichen(m):
    '''m是否有反对称性'''
    for i in range(len(m)):
        for j in range(len(m)):
            if(m[i][j]):
                if(m[j][i]):
                    return False
    return True

def chuandi(m):
    n=multi(m,m)
    if(ifInlude(n,m)):
        return True
    else:
        return False

def mi(m,n):
    '''求m的n次幂'''
    if(n==1):
        return m
    if(n==0):
        return I(len(m))
    return multi(mi(m,n-1),m)

def r(m):
    '''求自反闭包'''
    return bing(m,mi(m,0))

def s(m):
    '''对称闭包'''
    return bing(m,inverse(m))

def ms(m):
    '''求所有不同的幂'''
    ts=[mi(m,0)]
    ok=False
    time=1
    while(ok==False):
        ts.append(multi(m,ts[time-1]))
        time+=1
        for i in range(time):
            for j in range(i,time):
                if(ts[i]==ts[j] and i!=j):
                    ok=True
    return ts[0:time-1]

def countDiffMi(m):
    '''不同的幂的个数'''
    return len(ms(m))

def t(m):
    '''传递闭包（不同的幂）'''
    re=[]
    for i in ms(m):
        re=bing(re,i)
    return re
    
def ifdengjia(m):
    '''m是不是等价关系'''
    return zifan(m) and duichen(m) and chuandi(m)

def ifin(x,y,m):
    '''<x,y>是否在m里'''
    if(x>len(m) or y>len(m)):
        return False
    return m[x][y]
