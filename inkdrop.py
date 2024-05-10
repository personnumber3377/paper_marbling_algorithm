
CIRCLE_RESOLUTION = 200 # How many "circumference points" there are for each circle.
SCALE_FACTOR = 100 # Scale the coordinates by this much when drawing..

import math
import random

'''

def perpendicular( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

'''

# Just a helper function...

def perpendicular(a):
	#b = np.empty_like(a)
	b = [0.0, 0.0]
	b[0] = -a[1]
	b[1] = a[0]
	return tuple(b)

# Another helper to calculate "d"

def calc_d(P, A, N) -> float:
	P_minus_A = tuple((P[0]-A[0], P[1]-A[1]))
	dot_p = P_minus_A[0] * N[0] + P_minus_A[1] * N[1]
	d = abs(dot_p)
	return d

HEX = "0123456789ABCDEF"

def rand_color() -> str: # Returns a random color "#aabbcc"
	#return "#"+str("".join([random.choice(HEX) for _ in range(6)])) # Generate random hex color string
	# r, g and b are all the same.
	hex_thing = hex(random.randrange(0,256))[2:]

	if len(hex_thing) == 1: # 0x0 through 0xf:
		hex_thing = "0" + hex_thing

	assert len(hex_thing) == 2

	return "#"+(hex_thing*3)

class InkDrop:

	def __init__(self, r, x0, y0) -> None: # Constructor...
		self.r = r
		self.x0 = x0
		self.y0 = y0
		self.vertices = self.construct_vertices() # These are the very initial points on the circumference
		self.color = rand_color()
		return

	def construct_vertices(self) -> list: # Returns a list of tuples each of which describes an x,y point on the circumference of the circle.
		cur_angle = 0.0 # Initial calculation angle
		angle_step = 2*math.pi/(CIRCLE_RESOLUTION) # How many radians to step forward on each step
		out = []
		for i in range(CIRCLE_RESOLUTION):
			# Add point.
			dx = math.cos(cur_angle) * self.r
			dy = math.sin(cur_angle) * self.r
			new_point = tuple((self.x0+dx, self.y0+dy))
			out.append(new_point)
			cur_angle += angle_step # Update the angle.
		return out 

	def draw(self, t) -> None: # Render the shape. "t" is the turtle object we use to draw with.
		# Go through all of the vertices in order.
		t.color(self.color)
		t.fillcolor(self.color)
		t.penup()
		t.goto(self.vertices[0][0]*SCALE_FACTOR, self.vertices[0][1]*SCALE_FACTOR) # Go to the first vertex
		t.pendown()
		t.begin_fill()
		for vert in self.vertices[1:]: # Skip over first vertex here, because we already are there.
			t.goto(vert[0]*SCALE_FACTOR, vert[1]*SCALE_FACTOR)
		# Go back to the first vertex to close the loop.
		t.goto(self.vertices[0][0]*SCALE_FACTOR, self.vertices[0][1]*SCALE_FACTOR)
		t.end_fill()
		t.penup() # Stop drawing...
		return

	def marble(self, other) -> None: # This methods updates the vertices of this drop object using the other circle object.
		for i in range(len(self.vertices)): # Loop over each vertex.
			other_center = tuple((other.x0, other.y0))
			other_r = other.r
			#p_minus_c = tuple((self.x0 - other_center[0], self.y0 - other_center[1]))
			p_minus_c = tuple((self.vertices[i][0] - other_center[0], self.vertices[i][1] - other_center[1])) # self.vertices
			magnitude = math.sqrt(p_minus_c[0]**2 + p_minus_c[1]**2)
			root_val = math.sqrt(1 + (other_r * other_r) / (magnitude * magnitude))
			final_vec = tuple((other_center[0] + root_val * p_minus_c[0], other_center[1] + root_val * p_minus_c[1]))
			self.vertices[i] = final_vec
		return

	def tine(self, a, l, A, M) -> None: # This method applies the tine line transformation to this ink drop
		# "a" and "l" are both user defined parameters.
		
		# These are calculated from the mouse clicks:
		# A is the point on the line.
		# M is the unit vector in the direction of the line.

		#return # Just a stub for now.

		# "N is a unit vector perpendicular to L"

		# Let's calculate value of N

		# perpendicular

		N = perpendicular(M) # M is a unit vector in the direction of the line, so therefore we can just call "perpendicular" on it.

		for i in range(len(self.vertices)): # Loop through all points.
			P = self.vertices[i]
			d = calc_d(P, A, N)
			scalar_frac = (a * l) / (d + l)
			thing = tuple((M[0]*scalar_frac, M[1]*scalar_frac))
			self.vertices[i] = tuple((self.vertices[i][0] + thing[0], self.vertices[i][1] + thing[1]))

		return


