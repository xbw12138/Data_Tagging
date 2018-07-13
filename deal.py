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