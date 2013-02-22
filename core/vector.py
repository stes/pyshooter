import math

class Vector2D:
	'''
	A two component vector
	'''
	
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
	
	def copy(self):
		return Vector2D(self.x, self.y)

	def dot(self, other):
		return self.x*other.x + self.y*other.y
	
	def cross(self, other):
		return self.y * other.x - self.x * other.y
	
	def square(self):
		return self.dot(self)
	
	def len(self):
		return math.hypot(self.x, self.y)
	
	def projection(self, position, direction):
		'''
		projects this vector onto the line specified by the
		given position and direction vectors
		'''
		n = direction.normal()
		d = (n/n.len()).dot(self - position)
		xf = n*d
		return d, xf
	
	def list(self):
		return [self.x, self.y]
	
	def normal(self):
		'''
		returns a normal vector
		'''
		return Vector2D(-self.y, self.x)
	
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
	
	def __getitem__(self, index):
		if index == 0:
			return self.x
		elif index == 1:
			return self.y
		else:
			raise IndexError()
		
	def __setitem__(self, index, value):
		if index == 0:
			self.x = value
		elif index == 1:
			self.y = value
		else:
			raise IndexError()
	
	def __len__(self):
		return 2