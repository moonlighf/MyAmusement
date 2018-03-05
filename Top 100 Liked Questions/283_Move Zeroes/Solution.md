## 283 Move Zeroes
### 1. Question：  
 Given an array nums, write a function to move all 0's to the end of it while maintaining the relative order of the non-zero elements.

For example, given nums = [0, 1, 0, 3, 12], after calling your function, nums should be [1, 3, 12, 0, 0].

**Note:**   You must do this in-place without making a copy of the array. Minimize the total number of operations.


### 2.Answer:
（1） 首先是题目的意图：希望我们在不利用数组的复制的前提下完成数组元素的移动（删除和添加）。

（2） 题目中存在的陷阱，也是Python中初学者容易犯的错误，即在循环的过程中进行列表（数组）的删除

	#目的是为了删除a里面6的倍数的数
	a = [1, 2, 3, 12, 12, 5, 6, 8, 9]  
	for i in a:  
		if i % 2 == 0 and i % 3 == 0:  
			a.remove(i)  
			print(a)  
然后输出结果为： `[1, 2, 3, 12, 5, 8, 9]`

**发现12根本没有删除！！！**  

**这就是在循环删除的过程中改变了list的结构。**

举例理解：

① 循环到 `i = 12` （flag = 3）的时候，满足`if i % 2 == 0 and i % 3 == 0:`从而执行了`a.remove(12)`删除了列表里面的第一个`12`。

② 然后继续执行，这里` a =[1,2,3,12,5,6,8,9] `,接着执行的为`flag = 4`的时候，这时`i=5`,即跳过了原来列表a中的第四个元素，也就是我们需要删除的第二个12，所以出错。

**解决办法：**

一般对于这种问题有两种解决办法。（如果以后遇到继续补充）

① 利用复制，即将原有的列表做一个复制，然后在新列表中操作，循环条件则利用原来列表

	a = [1, 2, 3, 12, 12, 5, 6, 8, 9]  
	b = a[:]  
	for i in a:  
	        if i % 2 == 0 and i % 3 == 0:  
	            b.remove(i)  
	a = b  
	print(a)  

② 利用列表生成式。 其实这里还是开辟了新的内存空间。（也是本题中我的思路）

产生一个`temp_list`作为临时列表存储`nums`里面的非0元素；然后统计`nums`里面的0元素数量，生成一个全为0的list，然后两者组合。

### Code：
时间：59-60ms

	class Solution(object):
	    def moveZeroes(self, nums):
	        """
	        :type nums: List[int]
	        :rtype: void Do not return anything, modify nums in-place instead.
	        """
	        count_0 = nums.count(0)
	        temp_list = [x for x in nums if x != 0]
	        nums[:len(temp_list)] = temp_list
	        nums[len(temp_list):] = [0]*count_0

### 最短耗时时间（48ms）的人的Code：
	class Solution(object):
	    def moveZeroes(self, nums):
	        """
	        :type nums: List[int]
	        :rtype: void Do not return anything, modify nums in-place instead.
	        """
	        
	        n = len(nums)
	        
	        last_non_zero = -1
	        cur = 0
	        while cur < n:
	            if nums[cur] != 0:
	                last_non_zero += 1
	                nums[last_non_zero] = nums[cur]
	                cur += 1
	            else:
	                cur += 1
	        i = last_non_zero + 1
	        while i < n:
	            nums[i] = 0
	            i += 1
