
import turtle
from inkdrop import *
import time


CIRC_RADIUS = 0.5 # Radius of each circle when added.

new_circle = False
new_x = None
new_y = None

# These will be used in the creation of the tine lines when the user presses up.

p0 = None
p1 = None


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

def new_tine() -> None: # This will be called when the user presses the up arrow.
	global p0
	global p1
	global have_tine
	canv = turtle.getcanvas()
	x, y = canv.winfo_pointerx(), canv.winfo_pointery()
	print("x == "+str(x))
	print("y == "+str(y))
	if not p0: # p0 is not assigned, therefore just assign it and return
		p0 = tuple(())


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
	turtle.onkey(new_tine, "Up")
	turtle.listen()
	drops = [] # This is our main inkdrops list. We will use this to store all of our drop objects...
	#t.dot()
	while True: # Main program loop

		if not new_circle:
			# Just show each circle. This is because we haven't added a new circle.
			for drop in drops:
				drop.draw(t)
			#print("Drew all dots!")

		else:
			# Handle new circle.
			#print("new_circle == True")

			new_circ = InkDrop(CIRC_RADIUS, new_x, new_y)
			# Marble every other drop, before adding the new drop to the list.
			for drop in drops:
				drop.marble(new_circ)

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
