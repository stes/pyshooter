class Vector2D:

	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def dot(self, other):
		return self.x*other.x + self.y*other.y
	
	def square(self):
		return self.dot(self)
	
	def __add__(self, other):
		return Vector2D(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other):
		return Vector2D(self.x - other.x, self.y - other.y)
	
	def __mul__(self, other):
		if isinstance(other, Vector2D):
			return Vector2D(self.x * other.x, self.y * other.y)
		return Vector2D(self.x * other, self.y * other)
	
	def __div__(self, other):
		return Vector2D(self.x / other, self.y / other)
	
	def __pow__(self, other):
		return Vector2D(self.x**other, self.y**other)
	
	def __neg__(self):
		return Vector2D(-self.x, -self.y)
	
	def __pos__(self):
		return Vector2D(self.x, self.y)
	
	def __abs__(self):
		return Vector2D(abs(self.x), abs(self.y))
	
	def __str__(self):
		'''
		Converts the vector to a string
		'''
		return "(%f, %f)" % (self.x, self.y)

# The following lines should be processed
# correctly.

a = Vector2D(1, 2)
b = Vector2D(2, 3)
c = Vector2D(1, 42)

print a+b
print a-c
print a*c
print a.dot(c)
print a+(-b)
print c**2
print b/5.