题目：
  Given an array of integers, return indices of the two numbers such that they add up to a specific target.
  You may assume that each input would have exactly one solution, and you may not use the same element twice.
解释：
  就是说，给你个向量（列表），以及一个目标值，如果这个向量（列表）里面的两个元素加起来等于目标值，则输出这两个元素的下标
要求：
  每个输入的都应该有解决方法，而且相同的元素只能使用1次

例子：
          Given nums = [2, 7, 11, 15], target = 9,

          Because nums[0] + nums[1] = 2 + 7 = 9,
          return [0, 1].
          
思路：
其实最开始想到的是通过遍历，然后找到一个元素后将这个元素留下，再遍历剩下的，但是这样对于相同的元素就使用了两次以上，所以为了留下这个值，我选择了使用字典，这样能同时保留下标和所需要的另一个值，这样，遍历剩下的时候能通过和字典的比较来确认是否保留


其实这里也可以用python 里的枚举函数 `enumerate` 能同时得到下标和值。 
