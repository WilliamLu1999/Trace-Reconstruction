import random
import math
n = 10 # this is the length of the original string
q = 1/5 # the deletion probabilty for each bit 
d = 3 #the precision 
string_X = [] # the original string in an array form 

def function_1(n): # creating string X as a sequence offrom input n.
    i = 1
    while i <= n:
        x = random.random()
        if x < 0.5:
            x = 0
            string_X.append(0)
        else:
            string_X.append(1)
        i += 1
    return(string_X)

N = math.floor((8*(1+d)* math.log(n))/math.exp(-12*q*n)) # The number of traces we need
print(N)
def function_2(N,string_X): # creating N traces of X
    trace_all =[] # list of traces
    
    for i in range(N):
        trace = []
        for bit in string_X:
            y = random.random()
            if y < 1-q:    #determine each bit is remained or not
                trace.append(string_X[bit])
        trace_all.append(trace)
    return(trace_all)

    return trace_all

def function_3(trace_all): #reconstructing the original X string by using traces
    probability_list = []
    recovered_X = []
    for j in range(1,math.floor((1-3*q)*n+3*q)):
        f = 0  # number of times 1 is appearing at Yj
        for k in range(1,N+1):
            if trace_all[k][j] == 1:
                f += 1
        probability_list.append(f/N) # P(Yj = 1) = probability_list[j-1]
    for i in range(1,n+1):
        j = math.floor((1-3*q)*i + 3*q)
        prob_i_j = math.comb(i-1,j-1)*q^(i-j)*(1-q)^j
        summation = int(probability_list[j-1])
        for l in range(j,i-1):
            summation = summation - prob_i_j*int(recovered_X[l-1])
        


        if summation >= 3/4*prob_i_j:
            recovered_X[i-1] = 1
        else:
            recovered_X[i-1] = 0
    return recovered_X


def function_4(string_X, recovered_X):
    difference = 0
    for i in range (0,len(string_X)):
        if string_X[i] != recovered_X[i]:
            difference += 1
    return difference
            
print(function_1(10))
print(function_2(N,string_X))
print(function_3())

