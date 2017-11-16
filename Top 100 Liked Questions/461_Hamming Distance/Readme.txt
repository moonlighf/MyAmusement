Question:

The Hamming distance between two integers is the number of positions at which the corresponding bits are different.
Given two integers x and y, calculate the Hamming distance.
两个码字的对应比特取值不同的比特数称为这两个码字的海明距离。
举例如下：10101和00110从第一位开始依次有第一位、第四、第五位不同，则海明距离为3。

思路：
为了解决这个问题，需要两个步骤：
1.将所给整形数字转换为二进制
2.二进制码按照数位判断是否相同


关于第一点：
python里面转换二进制有内置函数 bin
>>> b = bin(3) 
>>> b
'0b11'
>>> type(b) #获取b的类型
<class 'str'>

关于第二点：
python里面有字符串的切片工具，
a[i-1:i] = b[i-1:i] ？？？   取出第 i-1 个字符和b的第 i-1 个字符 比较，不同则count +1


