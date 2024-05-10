
# Implementing the Paper Marbling Algorithm in python

Hi! Inspired by another coding train video here: https://www.youtube.com/watch?v=p7IGZTjC008&t=4s , I decided to try to implement it myself in python and see what happens. Ok, so it seems that paper marbling is an art-style. It is described here in detail in a wikipedia article: https://en.wikipedia.org/wiki/Paper_marbling . I think we are going to come across some fluid dynamics and shit like that soon enough...

## Understanding the marbling process on a high level

Ok, so let's get a feel for what we are about to do before jumping head first into coding...

Ok, so apparently there exists a mathematical solution, which doesn't involve any fluid dynamics, but approximates it good enough to look similar. This is also computationally less expensive than a full-blown fluid simulation.

Let's create the inkdrop object in a file called inkdrop.py .

Here is my very primitive start of the inkdrop object:

```

class InkDrop:

	def __init__(self, r, x0, y0) -> None: # Constructor...
		self.r = r
		self.x0 = x0
		self.y0 = y0
		return

	def update(self) -> None: # Update physics maybe... Stub for now.
		return



```

## Implementing the algorithm...

Ok, so let's say we drop an Inkdrop object on top of another inkdrop object. We want this new inkdrop to avoid the previously placed and sort-of "go around" it. Here is some of the mathematics, which describe this: https://people.csail.mit.edu/jaffer/Marbling/Mathematics and here is the very original "Mathematical Marbling" paper http://www.cad.zju.edu.cn/home/jin/cga2012/mmarbling.pdf .

First of all, we need to modify our inkdrop class to have a list of points which lie on the circumference, because we need those for the computation of the way how the inkrops "avoid" each other.

Here is the new modified inkdrop object:

```



CIRCLE_RESOLUTION = 10 # How many "circumference points" there are for each circle.
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


	def update(self) -> None: # Update physics maybe... Stub for now.
		return






```

let's test it out!

Here is the contents of my main.py file (for now) ... :

```



import turtle
from inkdrop import *
import time

def show_circle() -> None:

	t = turtle.Turtle() # Create a new turtle object.
	# __init__(self, r, x0, y0)
	drop = InkDrop(3, 0, 0) # Circle at (0,0) with radius 3.
	# Render the drop.

	drop.draw(t)

	time.sleep(5) # Wait for a bit for the user to see the result...

	return


if __name__=="__main__":
	# Main program entry point.

	show_circle()

	exit(0)


```

and it seems to work! Good!

## Handling of the new circles.

Let's create a loop, which just shows all of the circles over and over again... and then let's create an event handler which adds a new circle when the canvas gets clicked...


After a bit of fiddling around, I now have this as my main function:

```


import turtle
from inkdrop import *
import time


CIRC_RADIUS = 0.5 # Radius of each circle when added.

new_circle = False
new_x = None
new_y = None


def new_drop(x, y) -> None: # Will be called when the canvas gets clicked. Should create a new drop at x,y
	global drops # We need to modify this global variable, therefore we need this here.
	global new_x
	global new_y
	global new_circle
	print("Clicked at "+str(x)+", "+str(y)+" .")

	# When drawing, we scale by SCALE_FACTOR , therefore we need to divide by that here.

	new_x = x/SCALE_FACTOR
	new_y = y/SCALE_FACTOR
	new_circle = True
	return




def main_loop() -> None:
	global new_circle # We modify this.

	t = turtle.Turtle() # Create a new turtle object.
	# __init__(self, r, x0, y0)

	#t.tracer(0,0)
	turtle.tracer(0,0)
	#drop = InkDrop(3, 0, 0) # Circle at (0,0) with radius 3.
	# Render the drop.

	#drop.draw(t)

	turtle.onscreenclick(new_drop) # Setup click handlers
	drops = [] # This is our main inkdrops list. We will use this to store all of our drop objects...
	t.dot()
	while True: # Main program loop

		if not new_circle:
			# Just show each circle. This is because we haven't added a new circle.
			for drop in drops:
				drop.draw(t)
			#print("Drew all dots!")

		else:
			# Handle new circle.
			print("new_circle == True")

			new_circ = InkDrop(CIRC_RADIUS, new_x, new_y)
			drops.append(new_circ)
			new_circle = False
		time.sleep(0.01) # No need to draw faster than that

		turtle.update()

		t.clear()

	#time.sleep(5) # Wait for a bit for the user to see the result...

	return


if __name__=="__main__":
	# Main program entry point.

	main_loop()

	exit(0)


```

and it seems to work fine.

## Applying the formula for the new circles.

Ok, so now instead of automatically just putting the circle into the list, we need to modify the new circle with the pre-existing circles, such that the new circle avoids the pre-existing circles.

I actually got it the wrong way around, the new circle which we are adding is supposed to be an actual circle. It is the other circles which need to be modified to accommodate the new circle.

Let's program a method for our inkdrop object which updates the vertices with the given formula.

Here:

```

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


```

That seems to do the trick!

## Implementing line strokes

Ok, so that is quite good. I am thinking that we should also implement some other transformations while we are at it.






































