
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




