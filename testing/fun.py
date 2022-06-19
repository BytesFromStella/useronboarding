def A():
  return 1

def B(a):
  return a

def C(a, b = 2):
  return a + b

def D(*arg):
  return arg

def E(**kwargs):
  return kwargs

def F(a, b, *, c):
  return a + b + c

print( f"{A()=}" )
print( f"{B(1)=}" )
print( f"{C(1)=}" )
print( f"{C(1, 3)=}" )
print( f"{C(1, b = 4)=}" )

print( f"{D(1, 2, 3, 4, 5)=}" )

print( f"{E(a = 1, b = 2, c = 3)=}" )

print( f"{F(1, 2, c = 3)=}" )

list = [1,2,3,4,5]

print( f"{D(*list)=}" )
