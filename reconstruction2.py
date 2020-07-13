### Trace reconstruction by substring.
# This program finds out the i-th bit of the original message by using existing substring.
# July 12nd 2020
import random
import math

X =[]
w = 5   # length of the substring
q = 1/5 # deletion probability
r = 10  # (or 11 in this case) the position that y_j corresponds to in the original message X; (x_r = y_j)
u = 2   # the position that y_{j-w-1} corresponds to in the original message X; (x_u = y_{j-w-1})

i = 10
k = 1
v = 4
n = 100

def subsets(a,b): # this function produces different ways of match
    if a == 0:
        return [[]] # an empty list
    else:
        Lists = []
        for maxVal in range (a,b):
            ListsBeginning = subsets(a-1, maxVal - 1)
            for sublist in ListsBeginning:
                sublist.append(maxVal)
                Lists.append(sublist)
        return Lists

ListOfSubsets = subsets(w-2,r-u-1)

WaysMatch = 0
for subset in ListOfSubsets:
    IsThereAMatch = True
    for l in subset:
        if X[u+l-1] != X[i-v-w+l] :
            IsThereAMatch = False
    if IsThereAMatch:
        WaysMatch += 1 # number of ways choosing w-2 entries between u and r leading to correct match


prob_list_R_given_F = [] # the probability list of R given F
Probability_R_given_F = 0
Probability_F = n * math.exp(-2.2 * w * ((0.1-1.1*q)/1.1)**2) # for any a, more than 0.1w bits are deleted

for k in range(w,n):
    for u in range (i-v-1.1*w,i-v-w+1):   # to add up all possibility for FkRU
        for r in range (i-v,i-v+0.1*w):
            Probability_kru = WaysMatch * math.comb(u-1,k-w) * (1-q)**k * q**(r-k) # probability of Fk intersects r intersects u
            prob_list_R_given_F.append((Probability_kru/Probability_F)) # sum of the first part of S.

            for item in prob_list_R_given_F:
                Probability_R_given_F += item 
Probability_l_minus_r_j = 0

for l in range (r+1,i-1+1):
    Probability_l_minus_r_j += float((1/2)**(4*w))

S = float(Probability_R_given_F) * float(Probability_l_minus_r_j)

# predict P(Yj^new)
P_Y_new = 0


#Compare to the threshold
gamma = Probability_F
if P_Y_new <= gamma/2 + S + 3/4 *float((1/2)**(4*w))* prob_list_R_given_F:
    X[i-1] = 1
else:
    X[i-1] = 0







