



# c++中  (.h)头文件　　　(.cpp)源文件

# touch file{1..5}.cpp


import os
themes = ['1.初识linux shell','2.走进shell','３．.基本的bash shell 命令','4.更多的bash shell命令','５．理解shell','6.使用linux环境变量','７．理解linux文件权限','８．管理文件系统','９．安装软件程序','１０．使用编辑器','１１．构建基本脚本','１２．使用结构化命令','１３．更多的结构化命令','１４．处理用户输入','１５．呈现数据','１６．控制脚本','１７．创建函数','１８．图形化桌面环境的脚本编程','１９．初识sed和gawk','20.正则表达式','21.sed进阶','２２．gawk进阶','２３．使用其他shell','24.编写简单的脚本实用工具','２５．创建与数据库，web及电子邮件相关的脚本','２６．一些有意思的脚本']
base = "/home/lk/Recoding_Linux/linux命令行与shell脚本编程大全(第３版)/"
for i in themes:
    file_name = base + str(i)
    os.mkdir(file_name)