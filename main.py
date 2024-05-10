
import turtle
from inkdrop import *
import time
import random


CIRC_RADIUS = 0.5 # Radius of each circle when added.

new_circle = False
new_x = None
new_y = None

# These will be used in the creation of the tine lines when the user presses up.

p0 = None
p1 = None
new_tine = False


class WatchedKey:
	def __init__(self, key):
		self.key = key
		self.down = False
		turtle.onkeypress(self.press, key)
		turtle.onkeyrelease(self.release, key)

	def press(self):
		self.down = True

	def release(self):
		self.down = False



a_key = WatchedKey("a")

def new_drop(x, y) -> None: # Will be called when the canvas gets clicked. Should create a new drop at x,y
	global drops # We need to modify this global variable, therefore we need this here.
	global new_x
	global new_y
	global new_circle
	global a_key
	global p0
	global p1
	global new_tine

	print("Clicked at "+str(x)+", "+str(y)+" .")

	# Check if we are pressing "a" at the same time, if yes, then we have a tine.
	if a_key.down:
		print("Tine press!!!!!!!!!!!!")
		# Tine key press.
		if not p0: # assign p0 and return
			p0 = tuple((x/SCALE_FACTOR, y/SCALE_FACTOR))
			return
		elif not p1:
			p1 = tuple((x/SCALE_FACTOR, y/SCALE_FACTOR))
			# We should have p0
			assert p0 != None
			new_tine = True # Message the main loop about a new tine.

		return



	# When drawing, we scale by SCALE_FACTOR , therefore we need to divide by that here.

	new_x = x/SCALE_FACTOR
	new_y = y/SCALE_FACTOR 
	new_circle = True
	return 

def process_tine(drops, p0, p1) -> None: # This applies the tine transformation to each of the drops.

	#return # Just a stub for now.
	A = p0 # Just set A to the first point.
	p0_to_p1 = tuple((-p0[0]+p1[0], -p0[1]+p1[1]))
	# Divide by magnitude to get unit vec.
	mag = math.sqrt(p0_to_p1[0]**2 + p0_to_p1[1]**2) # Magnitude of the vector...
	# Now divide...
	unit_vec = tuple((p0_to_p1[0]/mag, p0_to_p1[1]/mag))
	M = unit_vec

	# Let's set alpha and lambda to just some constants.
	a = 0.3 # alpha
	l = 0.1 # lambda
	# def tine(self, a, l, A, M) -> None:
	# Now call tine() on each of the drop objects.
	for drop in drops:
		drop.tine(a, l, A, M)
	return

AUTOMODE = True # This automatically adds random stuff.

def main_loop() -> None:
	global new_circle # We modify this.
	# These two are required for the tine lines
	global p0
	global p1
	global new_tine

	t = turtle.Turtle() # Create a new turtle object.
	# __init__(self, r, x0, y0) 

	#t.tracer(0,0)
	turtle.tracer(0,0)
	#drop = InkDrop(3, 0, 0) # Circle at (0,0) with radius 3.
	# Render the drop.

	#drop.draw(t)



	turtle.onscreenclick(new_drop) # Setup click handlers
	#turtle.onkey(new_tine, "Up")
	turtle.listen()
	drops = [] # This is our main inkdrops list. We will use this to store all of our drop objects...
	#t.dot()
	count = 0
	while True: # Main program loop

		if not new_circle:
			# Just show each circle. This is because we haven't added a new circle.
			for drop in drops:
				drop.draw(t)
			#print("Drew all dots!")

		else:
			# Handle new circle.
			#print("new_circle == True")
			#MAX_RANGE = 0.5
			MAX_RANGE = 2
			radius = random.random() * MAX_RANGE
			new_circ = InkDrop(radius, new_x, new_y)
			# Marble every other drop, before adding the new drop to the list.
			for drop in drops:
				drop.marble(new_circ)

			drops.append(new_circ)
			new_circle = False

		if new_tine: # We have a new tine.
			#print("New tine line!")
			#print("p0 == "+str(p0))
			#print("p1 == "+str(p1))
			#p0 = 

			# Now process the tine line.

			process_tine(drops, p0, p1)

			new_tine = False
			p0 = None
			p1 = None

		#time.sleep(0.3) # No need to draw faster than that
		time.sleep(0.01)
		turtle.update()

		t.clear()

		if AUTOMODE:
			#if count > 1000: # Do not draw over a thousand times in auto mode
			#	continue
			# Generate random inkdrop...
			if random.random() < 0.9: # 10 % of a random inkdrop...
				new_circle = True
				new_x = (random.choice([1, -1])) * (random.random() * 6)
				new_y = (random.choice([1, -1])) * (random.random() * 6)
				count += 1
				print("Count == "+str(count))

			# Random thing.


	#time.sleep(5) # Wait for a bit for the user to see the result...

	return


if __name__=="__main__":
	# Main program entry point.
	
	main_loop()

	exit(0)
