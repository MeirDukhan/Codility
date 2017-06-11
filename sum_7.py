

# Write a functions that gets a number and return the sum of all numbers that
# can be divided by 7 from 0 to that given number. 

def sum_7(n):
    pass
    i = 0 
    s7 = 0
    while i <= n: 
        if i % 7 == 0:
            s7 += i
            print i
        i += 1 

    return s7 

x = sum_7(30)
print "Sum of numbers divising by 7 up to 30: ", x 


