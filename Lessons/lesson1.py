# Documentation
# Python website - https://www.python.org/
# Wiki - https://docs.python.org/
# Built-In Functions - https://docs.python.org/3/library/functions.html


#Literals
True  # 1
None  # Null,Nil,Nothing
False # 0


10      #Int
11.35   #Float
3e-10   #FLoat
3+8.5j  #Complex


"Hello World" #String
f"Hi Everyone, {'Hello World'}" #Format String
[1,2,3,4,5] # List
(2,3,4)     # Tuple
{"name":"Sun","mass":1.989e30} # Dictionary

#Arithmetic operations
2 + 3  # add
2 - 3  # subtract
2 * 3  # multiply
2 / 3  # float divide
7 // 3 # integer divide
2 ** 3 # power
2 % 3  # modulus
5 * 8 / 2 + 8 ** 2 - 4 * 11 + 2# PEMDAS


#Bitwise operations
1<<8   # bitshift left
256>>8 # bitshift right
170&5  # bitwise And
170|5  # bitwise Or
~5     # complement
170^85 # bitwise Xor

#Comparisons
5 == 5    # Equals
3 != 5    # Not Equal
5 > 3     # Greater Than
2 < 3     # Less Than
4 >= 4    # Greater Than or Equal
1 <= 18   # Less Than or Equal
not False #  Negate

x = 5
b = x

b is x    # Check object equality
3 in [1,2,3,4] # Check membership


#Variables
x = 3    # assign Int 3 to x
y = 1+2j # assign complex literal to y

#Flow control
# if elif else
if x == 3:
    print("Three")
elif x > 3:
    print("Bigger than Three")
else:
    print("Smaller than Three")

# while
count = 0
while count < 10:
    print(count)
    count = count + 1

# for
for i in [0,1,2,3,4,5,6,7,8]:
    print(i)

# continue
for i in range(25):
    if i < 10:
        continue
    else:
        print(i)

# break
for i in range(25):
    if i > 10:
        break
    else:
        print(i)
        
# pass
for i in range(25):
    pass

#functions
# call a built-in function
x = range(20)

# define a function
def fun(x):
    return x + 1

fun(5) # call defined function.


#Classes
class Car:
    def __init__(self, make:str, model:str, year:int):
        self.make = make
        self.model = model
        self.year = year
    
    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class CarOwner: 
    cars = []
    def __init__(self, name:str):
        self.name = name

    def registerCar(self, car:Car):
        self.cars.append(car)

    def __str__(self):
        return f"{self.name}:Cars {len(self.cars)}"

owners = []
owner1 = CarOwner("Micah")
owner1.registerCar(Car("Robin", "Reliant", 1980))
owners.append(owner1)

for owner in owners:
    print(owner)
    for car in owner.cars:
        print("%s" % car)

