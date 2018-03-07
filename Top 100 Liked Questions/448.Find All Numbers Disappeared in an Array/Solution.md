## 448. Find All Numbers Disappeared in an Array


### 1. Question:
 
Given an array of integers where 1 ≤ a[i] ≤ n (n = size of array), some elements appear twice and others appear once.

Find all the elements of [1, n] inclusive that do not appear in this array.

Could you do it without extra space and in O(n) runtime? You may assume the returned list does not count as extra space.

### 2. Answer:
(1) 　明白题目的意图：给定了一个整数列表，里面的元素大于1小于列表大小，且存在一些元素出现两次。

**目的**是找出[1, n]中没有在这个数组里面没有出现的元素。

**要求**不能有额外的空间并且时间复杂度为O（n）

（2）**那些可能有用的东西:**　① 这样一个一维数组（列表）重复的数字的量就是缺少的数字的量，也就是重复的数字和缺少的数字可能存在某种关系

a）第一想法是利用set的交集，也就是将list转换为set（一个有序的集合），然后计算两个set的交集，就是远nums缺少的数字，从而有了方法一。

（1）方法一：283 ms - 300+ ms

	return list(set(range(1,len(nums)+1)) - set(nums))
b）根据**那些可能有用的东西：**里面的想法去思考，就是找到缺少的数据和重复的数据的关系。如果遍历，那么重复的数据就需要计算两遍，这样可能有用。于是有了方法二。

（2）方法二304 ms - 350 ms

	for i in xrange(len(nums)):
		index = abs(nums[i]) - 1
		nums[index] = - abs(nums[index])
	return [i + 1 for i in range(len(nums)) if nums[i] > 0]

虽然可能方法二更符合题意——即没产生额外的空间，但是方法二的平均耗时是要高于方法一的。



#### 可能还有更好的方法，等待我去思考！
