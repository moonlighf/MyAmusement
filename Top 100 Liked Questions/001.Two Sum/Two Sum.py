class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        if len(nums) ==0:
            return False
        buf = {}
        for i in xrange(0,len(nums)):
            if nums[i] in buf:
                return [buf[nums[i]], i]
            else:
                buf[target - nums[i]] = i
