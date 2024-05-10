
CIRCLE_RESOLUTION = 20 # How many "circumference points" there are for each circle.
SCALE_FACTOR = 100 # Scale the coordinates by this much when drawing..
import math

class InkDrop:

	def __init__(self, r, x0, y0) -> None: # Constructor...
		self.r = r
		self.x0 = x0
		self.y0 = y0
		self.vertices = self.construct_vertices() # These are the very initial points on the circumference
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
		t.penup()
		t.goto(self.vertices[0][0]*SCALE_FACTOR, self.vertices[0][1]*SCALE_FACTOR) # Go to the first vertex
		t.pendown()
		for vert in self.vertices[1:]: # Skip over first vertex here, because we already are there.
			t.goto(vert[0]*SCALE_FACTOR, vert[1]*SCALE_FACTOR)
		# Go back to the first vertex to close the loop.
		t.goto(self.vertices[0][0]*SCALE_FACTOR, self.vertices[0][1]*SCALE_FACTOR)
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


