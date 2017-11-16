class Solution(object):
    def hammingDistance(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: int
        """
        binx = bin(x)
        biny = bin(y)
        binx = binx[2:]
        biny = biny[2:]
        lengthx = len(binx)
        lengthy = len(biny)
        count = 0
        if lengthx <= lengthy:
            binx = binx.zfill(lengthy)
            for i in range(0, lengthy):
                if binx[i] != biny[i]:
                    count += 1
        else:
            biny = biny.zfill(lengthx)
            for i in range(0, lengthx):
                if binx[i] != biny[i]:
                    count += 1
        return count