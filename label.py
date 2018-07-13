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