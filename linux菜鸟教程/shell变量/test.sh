#! /bin/bash


your_name="runoob"
# 使用双引号拼接

greeting="hello, "$your_name" !"
greeting_1="hello, ${your_name} !"
echo $greeting  $greeting_1



string="abcd"
echo ${#string} #输出 


string="runoob is a great site"
echo ${string:1:4} # 输出 unoo
