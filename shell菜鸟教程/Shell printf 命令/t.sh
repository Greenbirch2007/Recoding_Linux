#! /bin/bash

printf "%-10s %-8s %-4s\n" 姓名　性别　体重kg
printf "%-10s %-8s %-4.2s\n" 杨过　男　　66.68



# format-string为双引号
printf "%d %s\n" 1 "abc"


# 单引号与双引号效果一样

printf '%d %s\n' 1 "abc"

# 没有引号也可以输出

printf %s abcdef

# 格式指定了一个参数，但多出的参数仍然会按照格式输出，format-string被重用

printf %s abc def

printf "%s\n" abc def

printf " %s %s %s\n" a b c d e f h i j

# 如果没有 arguments,那么%s 用null代替，%d　用0代替
