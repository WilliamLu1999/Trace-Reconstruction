### Trace reconstruction by substring.
# This program finds out the i-th bit of the original message by using existing substring.
# July 12nd 2020
import random
import math

print("hi")
n = 100
q = 1/40 # deletion probability
d = 1

# r = 10  # (or 11 in this case) the position that y_j corresponds to in the original message X; (x_r = y_j)
# u = 2   # the position that y_{j-w-1} corresponds to in the original message X; (x_u = y_{j-w-1})
w = 20
#w = int((6+3*d)*math.log(n))   # length of the substring
i = 95
v = 70
#v = int(4+(1+0.1*w)/q)
j = int((v-0.1*w)*(1-3*q))
# N = (2**(2*w+28)/(1-q)**w) * (math.log(n)*(1+d)+math.log(2)) # number of traces required 
# which is 2.0008099468643687e+35
N = 1000000

def function_1(n): # creating string X as a sequence offrom input n.
    string_X = [] # the original string in an array form
    i = 1
    while i <= n:
        x = random.random()
        if x < 0.5:
            x = 0
            string_X.append(0)
        else:
            string_X.append(1)
        i += 1
    return string_X
    
string_X = function_1(n) # Get the original X
w_substring = []


# get the substring
for position in range(i-v-w,i-v):
    w_substring.append(string_X[position])


def subsets(a,b): # this function produces different ways of match
    if a == 0:
        return [[]] # an empty list
    else:
        Lists = []
        for maxVal in range (a,b+1):
            ListsBeginning = subsets(a-1, maxVal - 1)
            for sublist in ListsBeginning:
                sublist.append(maxVal)
                Lists.append(sublist)
        return Lists

print(subsets(2,4))

# Finding out the probability of R = r intersects F
prob_list_R_on_F = []
for r in range(i-v-1, int(i-v+0.1*w)):
    Probability_R_on_F = 0
    print('r is'+str(r))
    for u in range (int(i-v-1.1*w)-1, i-v-w+1):
        # check if x_u and x_r are matching the substring we want.
        if string_X[u] == w_substring[0] and string_X[r] == w_substring[w-1] :
            WaysMatch = 0
            ListOfSubsets = subsets(w-2,r-u-1)
            print(r-u-1)
            for subset in ListOfSubsets:
                IsThereAMatch = True
                for l in range(1,w-1):
                    if string_X[u+subset[l-1]] != w_substring[l] :
                        IsThereAMatch = False
                if IsThereAMatch:
                    print('theres a match')
                    WaysMatch += 1
            for k in range(w,r+2):
                Probability_kru = WaysMatch * math.comb(u,k-w) * (1-q)**k * q**(r+1-k)
                Probability_R_on_F += Probability_kru
    prob_list_R_on_F.append(Probability_R_on_F)

Probability_F = 0
prob_list_R_given_F = [] 
Probability_R_given_F = 0

S = 0
threshold_end = 0 #latter part of the threshold (similiar to S)
# to get S
for r in range(i-v-1, int(i-v+0.1*w)):
    print('r is '+str(r))
    Probability_F += prob_list_R_on_F[r-i+v] 

for r in range(i-v-1, int(i-v+0.1*w)):
    for l in range (r+2,i):
        S += prob_list_R_on_F[r+1-i+v]/Probability_F * (math.comb(l-r-2,j-1)*q**(l-r-1-j)*(1-q)**j) * string_X[l-1]
    threshold_end += prob_list_R_on_F[r+1-i+v]/Probability_F * (math.comb(i-r-2,j-1)*q**(i-r-1-j)*(1-q)**j)
    
# predict P(Yj^new=1)
P_Y_new = 0 
number_Y_j_new_0 = 0
number_Y_j_new_1 = 0
Y_j_new = 0

def generate_trace():
    trace =[]
    for bit in string_X:
        y = random.random()
        if y > q:
            trace.append(bit)
    return trace


# Convert w substring to string form
str_sub_1 = ''.join(str(bit)for bit in w_substring)
print(str_sub_1)
print(string_X)
for l in range(1,N+1):
    print(l)
    trace = generate_trace()
    str_trace_1 = ''.join(str(bit)for bit in trace) # Convert each trace to string in order to check if the substring is in it
    print(str_trace_1)
    if str_sub_1 in str_trace_1: # if the substring is in the trace
        print(True)
        # then know where the substring is in the trace. which directly returns the index
        where = str_trace_1.find(str_sub_1)
        # Y_j^new is the bit number j after the end of the substring in the trace
        Y_j_new = trace[where+int(j)]
	    # if Y^j_new is 1 increase number_Y_j_new_1
        if Y_j_new == 1:
            number_Y_j_new_1 += 1
        # if Y^j_new is 0 increase number_Y_j_new_0   
        if Y_j_new == 0:
            number_Y_j_new_0 += 1

print(number_Y_j_new_1,number_Y_j_new_0)
P_Y_j_new_equal_to_1 = float(number_Y_j_new_1/(number_Y_j_new_0+number_Y_j_new_1))


#Compare to the threshold
error_gamma = n*2*(1.4*(q**0.1))**w/(1-q)**w
recovered_X = 0
if P_Y_j_new_equal_to_1 <= S + 3/4 * threshold_end:
   recovered_X = 0
else:
    recovered_X = 1
    
print(recovered_X)
print(error_gamma)
print(string_X[i-1])
print(P_Y_j_new_equal_to_1)
print(S)
print(threshold_end)