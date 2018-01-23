# File: Hello.py

print ("Hello World!")
# a = 1 + 2 + 3 # + \
    # 4 + 5 + 6 + \
    # 7 + 8 + 9
a = (1 + 2 + 3 +
    4 + 5 + 6 +
    7 + 8 + 9)
colors = ['red',
          'blue',
          'green']
print (len(colors))
# for i in len(colors):
if colors[0] == 'red' :
	print("COLOR iS RED :::")
	print(len(colors))
	print("COLOR RED Turned Orange:::")
	colors[0] = 'orange'
	print(colors[0])
"""This is also a
perfect example of
multi-line comments"""

def double(num):
    return 2*num
    # """Function to double the value"""
print (double(4)) # to print the double value of a integer

print (double("num")) # to print the double value of a string "numnum"

print(double.__doc__) # to print the document string first statement of a method

a = 5
print(a, "is of type", type(a))

a = 2.0
print(a, "is of type", type(a))

a = 1+2j
print(a, "is complex number?", isinstance(1+2j,complex))


a = 1234567890123456789
print(a) # can store any digit integer as per the 
b = 0.1234567890123456789
print(b) # can store any digit flot decimal upto 15 decimals
c = 1+2j
print(c) # c is a complex number


# Dealing with arrays(Mutable-> can be edited)
print("Arrays::::")
a = [5,10,15,20,25,30,35,40]

# a[2] = 15
print("a[2] = ", a[2])

# a[0:3] = [5, 10, 15]
print("a[0:3] = ", a[0:3])

# a[5:] = [30, 35, 40]
print("a[5:] = ", a[5:])



# Dealing with Tuples(Immutable-> non editable)
print("Tuples::::")
t = (5,'program', 1+3j)

# t[1] = 'program'
print("t[1] = ", t[1])

# t[0:3] = (5, 'program', (1+3j))
print("t[0:3] = ", t[0:3])

# Generates error
# Tuples are immutable
# t[0] = 10

print("Strings::::")

s = 'Hello world!'

# s[4] = 'o'
print("s[4] = ", s[4])

# s[6:11] = 'world'
print("s[6:11] = ", s[6:11])

# Generates error
# Strings are immutable in Python
# s[5] ='d'

print("Sets::::")
a = {5,2,3,1,4}

# printing set variable
print("a = ", a)

# data type of variable a
print(type(a))

a = {1,2,2,3,3,3}
# printing set variable
print("a = ", a)
print(a[0]) # set doesn't support indexing