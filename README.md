# 机器学习 人工标注样本工具Python+OpenCV

## 应用场景
最近小伙伴有个需求，需要对训练样本进行人工标注，需要框选出复杂场景图片中的气压表的部分，并标注出气压值，同时还需要知道气压表在图像中的位置，为解决这一问题，利用OpenCV的 鼠标框选的功能实现这一小工具

## 使用说明
### 1.目录
![这里写图片描述](https://github.com/xbw12138/Data_Tagging/blob/master/res/WX20180713-123008%402x.png)
deal.py  人工标注主程序 <br>
generate_data  存放标注结果图像 <br>
label   存放图像对应标注文本信息 <br>
label.py  根据generate_data数据生成图像与标注信息相对应文本信息的程序 <br>
original_data  存放原始图像数据 <br>

---

### 2.运行环境
Python 2.7 <br>
OpenCV 3.1

---

### 3.使用方法
#### 3.1标注图像
启动程序 执行 `python deal.py` 后
会打开original_data文件夹下的一张图片<br>
![这里写图片描述](https://github.com/xbw12138/Data_Tagging/blob/master/res/WechatIMG134.jpeg)
例如这样，我们现在需要在图像上手动圈出气压表的位置，鼠标按下时记录一个起点，松开时记录一个终点，这样就绘制了一个矩形，把气压表框选出来。<br>
![这里写图片描述](https://github.com/xbw12138/Data_Tagging/blob/master/res/zyh_1_439_220_823_589_100.00.jpg)
没有截取运行的过程图片，框选完应该是蓝色，这时会弹出一个提示框，要求我们选择是否框选正确的提示。<br>
![这里写图片描述](https://github.com/xbw12138/Data_Tagging/blob/master/res/WechatIMG408.png)
例如这样，当我们选择错误，就会要求重新在这张图上框选，当我们确定了框选位置，就会弹出输入气压值的输入框，如下图。<br>
![这里写图片描述](https://github.com/xbw12138/Data_Tagging/blob/master/res/WechatIMG404.png)
输入气压值后，我们这张处理好的图片就会存入generate_data文件夹中，图像命名为标注信息。例如 ：  zyh_1_439_220_823_589_100.00.jpg  <br>
439，220为左上角坐标，823，589为右下角坐标，100.00位气压值。 <br>
这样我们就标注好一张图了，他会自动弹出第二张图，同上处理，直到处理完所有图片。

---

#### 3.2生成图像对应标注信息

启动程序 执行 `python label.py` 就好了，生成的信息在label/label.txt中

---

### 4.代码
deal.py

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import cv2
import Tkinter as tk
global point1,point2
global pressure,ensure
def write(entry,win):
    global pressure
    pressure = entry.get()
    win.destroy()
def confirm(confirm,win):
    global ensure
    ensure = confirm
    win.destroy()
def createWinSure():
    win=tk.Tk()
    label=tk.Label(win,text="确认图像标注正确",bg="white",fg="black")
    label.pack()
    buttony=tk.Button(win,text="正确",command=lambda:confirm(True,win)) #收到消息执行这个函数
    buttony.pack()#加载到窗体，
    buttonn=tk.Button(win,text="错误",command=lambda:confirm(False,win)) #收到消息执行这个函数
    buttonn.pack()#加载到窗体，
    win.mainloop()
def createWinWri():
    win=tk.Tk()
    label=tk.Label(win,text="请输入压强:",bg="white",fg="black")
    label.pack()
    entry=tk.Entry(win,width=50,bg="white",fg="black")
    entry.pack()
    button=tk.Button(win,text="确认",command=lambda:write(entry,win)) #收到消息执行这个函数
    button.pack()#加载到窗体，
    win.mainloop()
def on_mouse(event, x, y, flags, param):
    global point1,point2
    global ensure
    global pressure
    img = param[0]
    index = param[1]
    img2 = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:         #左键点击
        point1 = (x,y)
        cv2.circle(img2, point1, 10, (0,255,0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_MOUSEMOVE and (flags & cv2.EVENT_FLAG_LBUTTON):               #按住左键拖曳
        cv2.rectangle(img2, point1, (x,y), (255,0,0), 5)
        cv2.imshow('image', img2)
    elif event == cv2.EVENT_LBUTTONUP:         #左键释放
        point2 = (x,y)
        cv2.rectangle(img2, point1, point2, (0,0,255), 5) 
        #ensure = raw_input("确认图像标注正确,输入y or n :")
        createWinSure()
        if ensure:
            createWinWri()
            #pressure = raw_input("请输入压强:")
            cv2.imwrite('./generate_data/zyh_'+str(index)+'_'+str(point1[0])+'_'+str(point1[1])+'_'+str(point2[0])+'_'+str(point2[1])+'_'+pressure+'.jpg', img2)
            cv2.imshow('image', img2)
            cv2.destroyAllWindows()
        else :
            print '请在图片上重新框选!'
def main():
    for root, dirs, files in os.walk('./original_data/'): 
       for i in range(0,len(files)):
            img = cv2.imread('./original_data/'+files[i])
            cv2.namedWindow('image')
            cv2.setMouseCallback('image', on_mouse,[img,i+1])
            cv2.imshow('image', img)
            cv2.waitKey(0)
    

if __name__ == '__main__':
    main()
```
---
label.py

```python
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os

def main():
    of = open("./label/label.txt","w")
    for root, dirs, files in os.walk('./generate_data/'): 
       for f in files:
           fo = f
           f = f[:-4]
           f_list = f.split('_')
           _,_,x1,y1,x2,y2,pressure = f_list
           label = '('+x1+','+y1+') ('+x2+','+y2+') '+pressure
           tmp = fo+' '+label+'\n'
           of.writelines(tmp)
    of.close()
            
    

if __name__ == '__main__':
    main()
```







