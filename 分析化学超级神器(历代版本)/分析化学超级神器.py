from math import log10
from pathlib import Path
import json
import decimal
active = True
# decimal.getcontext(rounding = decimal.ROUND_HALF_UP).
while active:
    yixiang = input("\t输入“1”进行实验数据分析\n\t输入“2”进行酸碱滴定分析\n\t")
    def baoliuxiaoshu(value):
            value = decimal.Decimal(f"{value}")
            try:
                value = value.quantize(decimal.Decimal(f"{weishu}"),decimal.ROUND_HALF_UP)
            except decimal.InvalidOperation:
                print("\t\t\t小数位数都输不来了,这边建议把小脑捐了吧")
            else:
                return value
    if yixiang == "1":
        weishu = input("请输入需要保留的小数位数,例如“0.01”")
        path = Path("实验数据.txt")
        while 1:
            try:
                data = input("请以输入需要分析的数据\n\t")
                datal = data.split(",")        #关键的一步，split拆分后得到一个列表(但列表中的元素还是字符串形式，例如["38.12","38.21","38.46","38.13"])
                lastdata = [float(datal[i]) for i in range(len(datal))]  #将列表中的元素转换为严格的数字，得到一个数组
            except ValueError:
                    print("\t\t没整对\n")
            else:
                
                content = json.dumps(lastdata)
                path.write_text(content)        #使人可读
                content1 = json.loads(content)
                # print(content1)
                l ,sum1 = len(content1), 0
                avedata = sum(content1) / l   #平均值
                for  exdata in content1:
                    sum1 += (exdata - avedata) ** 2
                try:
                    ans = (sum1 / (l - 1)) ** (1/2)    #样本标准偏差
                    ans = baoliuxiaoshu(ans)
                    jicha = max(content1) - min(content1) 
                    jicha = baoliuxiaoshu(jicha)               #极差
                    pingjunpiancha = sum(max(value - avedata,-value + avedata) / l for value in content1) #平均偏差
                    avedata = baoliuxiaoshu(avedata)
                    pingjunpiancha = baoliuxiaoshu(pingjunpiancha)   #标准偏差
                    try:
                        xiangduipingjun = pingjunpiancha / avedata *100
                        xiangduibiaozhun = ans / avedata *100       #计算带“相对”的都要乘以100%
                    except TypeError :
                        print("\t\t\t我没开玩笑\n\t\t\t我爱嗦石化")
                        continue
                    else:
                        xiangduipingjun = baoliuxiaoshu(xiangduipingjun)
                        xiangduibiaozhun = baoliuxiaoshu(xiangduibiaozhun)


                except ZeroDivisionError:
                    print("\n\t数据就一个你分析个啥?\n")
                else:
                    print(f"分析结果\n平均值\tx为\t{avedata}")
                    print(f"分析结果\n平均偏差\tx为\t{pingjunpiancha}")
                    print(f"\t\n相对平均偏差\td为\t{xiangduipingjun}%")
                    print(f"\t\n样本标准偏差\ts为\t{ans}")
                    print(f"\t\n相对标准偏差\tsr为\t{xiangduibiaozhun}%")
                    print(f"\t\n极差\tR为\t{jicha}")
                    
                    
                    active = input("是否继续进行数据分析,不需要的话请输入“停止”")
                    if active == "停止":
                        break
    elif yixiang == "2":
        kw = 1.0 * 10 ** -14
        print("\n\t计算一元弱酸/碱PH请输入“1”\t(一般二元弱酸/碱也可以用这个)")
        print("\t计算两性物质PH请输入“2”")
        print("\t计算酸碱缓冲溶液PH请输入“3”")
        yixiang = input("\t")
        if yixiang == "1":
            try:
                c = float(input("请输入两性物质的浓度或logc\n科学计数法用'xe-n'表示\n\t"))
                if c < 0 :
                    c = 1*10**(c)
                ka = float(input("请输入酸/碱的电离常数或PKa\n\t"))
                if ka >= 1:
                    ka = 1*10**(-ka)
                weishu = input("请输入需要保留的小数位数,例如“0.01”\n\t")
           
                if c * ka >= 10 * kw and c / ka >= 105:
                    CH = (c * ka)**(1/2)                    #具体算法
                elif c * ka >= 10 * kw and c / ka < 105:
                    CH = (-ka + (ka**2 + 4*c*ka)**(1/2))/2
                elif c * ka < 10 * kw and c / ka >= 105:
                    CH = (c * ka + kw)**(1/2)
                PH = -log10(CH)             #取对数
            except ValueError:
                print("\t没整对")
                continue
            else:
                s_or_j = input("该物质是酸还是碱\n\t")
                if s_or_j == "酸" or "s":
                    print(f"PH值为 {baoliuxiaoshu(PH)}")
                elif s_or_j == "碱" or "j":
                    PH = 14 - PH
                    print(f"PH值为 {baoliuxiaoshu(PH)}")
                else:
                    print("没整对")
                    continue
        elif yixiang == "2":
            try:
                c = float(input("请输入两性物质的浓度或logc\n科学计数法用'xe-n'表示\n\t"))
                if c < 0 :
                    c = 1*10**(c)
                ka1 = float(input("请输入两性物质的一级电离常数或PKa1\n\t"))
                if ka1 >= 1:                                #天才般的想法
                    ka1 = 1*10**(-ka1)
                ka2 = float(input("请输入两性物质的二级电离常数或PKa2\n\t"))
                if ka2 >= 1:
                    ka2 = 1*10**(-ka2)
                weishu = input("请输入需要保留的小数位数,例如“0.01”\n\t")
            except ValueError :
                print("没整对")
                continue

            if c * ka2 > 10*kw and c > 10*ka1:
                CH = (ka1 * ka2) ** (1/2)
            elif c * ka2 > 10*kw:
                CH = (c * ka1 * ka2 / (c + ka1)) ** (1/2)
            else:
                CH = (ka1*(c*ka2 + kw)/(c + ka1)) ** (1/2)
            PH = -log10(CH)
            print(f"PH值为 {baoliuxiaoshu(PH)}")
        elif yixiang == "3":
            try:
                c1 = float(input("请输入缓冲对酸的浓度或logc\n科学计数法用'xe-n'表示\n\t"))
                if c1 < 0 :
                    c1 = 1*10**(c1)
                c2 = float(input("请输入缓冲对碱的浓度或logc\n\t"))
                if c2 < 0 :
                    c2 = 1*10**(c2)
                ka = float(input("请输入缓冲溶液的酸常数或PKa\n\t"))
                if ka >= 1:
                    ka = 1*10**(-ka)
            except ValueError:
                print("没整对")
                continue
            else:
                CH = c1/c2*ka
                if c1 > 10*CH and c2 > 10*CH:
                    try:
                        PH = -log10(CH)
                    except ValueError:
                        print("没整对")
                        continue
                else:
                    s_or_j = input("该物质呈酸性还是碱性\n\t")
                    if s_or_j == "酸性" or s_or_j == "酸" or s_or_j == "s":
                        CH = (-c2-ka +((c2 + ka)**2 + 4*ka*c1)**(1/2))/2
                    elif s_or_j == "碱性" or s_or_j == "碱" or s_or_j == "j":
                        CH = 10**-14 + c1*ka + (((10**-14 + c1*ka)**2 + 4*c2*ka*10**-14))/2*c2
                    else:
                        print("没整对")
                        continue
                    try:
                        PH = -log10(CH)
                    except ValueError:
                        print("没整对")
                        continue
            weishu = input("请输入需要保留的小数位数,例如“0.01”\n\t")
            print(f"PH值为 {baoliuxiaoshu(PH)}\n")
         

            

        

    else:
        print("\n\t你小汁,找茬是吧\n\t")
        yixiang1 = input("想退出请输入“退出”\t")
        if yixiang1 == "退出":
            active = False


     





    