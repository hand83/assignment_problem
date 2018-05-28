# -*- coding: utf-8 -*-
"""
Created on Sun May 27 2018
@author: Andras Horvath

Testing script for assingment problem
"""
from assignment_problem import *

test3 = ["(1,2,1)","(4,1,5)","(5,2,1)"]
# solution: "(1-1)(2-2)(3-3)"
test4 = ["(13,4,7,6)","(1,11,5,4)","(6,7,2,8)","(1,3,5,9)"]
# solution: "(1-2)(2-4)(3-3)(4-1)"
test6a = ["(6,16,22,9,13,3)","(11,29,13,39,18,30)","(1,24,7,44,12,16)",
         "(2,44,30,21,15,19)","(8,19,45,39,46,20)","(47,6,25,8,29,23)"]
# solution: "(1-6)(2-3)(3-5)(4-1)(5-2)(6-4)"
# or:       "(1-6)(2-5)(3-3)(4-1)(5-2)(6-4)"
test6b = ["(1,7,22,38,13,60)","(12,29,38,47,56,9)","(52,41,30,29,18,7)",
          "(6,9,19,33,52,15)","(53,42,31,20,9,27)","(64,52,40,38,26,14)"]
# solution: "(1-2)(2-1)(3-4)(4-3)(5-5)(6-6)"
test6c = ["(24,9,13,37,12,5)","(30,17,28,39,18,6)","(66,16,32,44,49,10)",
          "(53,43,13,21,19,20)","(8,50,45,38,46,19)","(26,47,25,14,29,23)"]

print OptimalAssignments(test3)
print OptimalAssignments(test4)
print OptimalAssignments(test6a)
print OptimalAssignments(test6b)
print OptimalAssignments(test6c)