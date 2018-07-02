'''
    question:
        Given two arrays, write a function to compute their intersection.
        取两个列表的集合
    解题思路:
        1.先转换为集合，使用集合的取交集方法
        2.再转化为列表
'''
class Solution:
    def intersection(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        
        return list(set(nums1) & set(nums2))

