
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



























