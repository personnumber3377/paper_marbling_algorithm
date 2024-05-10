
import turtle
from inkdrop import *
import time

def main_loop() -> None:

	t = turtle.Turtle() # Create a new turtle object.
	# __init__(self, r, x0, y0) 

	drop = InkDrop(3, 0, 0) # Circle at (0,0) with radius 3.
	# Render the drop.

	drop.draw(t)


	drops = [] # This is our main inkdrops list. We will use this to store all of our drop objects...

	while True: # Main program loop

	#time.sleep(5) # Wait for a bit for the user to see the result...

	return


if __name__=="__main__":
	# Main program entry point.
	
	main_loop()

	exit(0)
