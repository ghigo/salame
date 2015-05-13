# Fridge main

from led import Led

def test():
	print "test function"


# main
print "Welcome to Fridge!"

test()
led = Led(11)
# led.blink(10)
# led.blink_for(5, 0.15, 0.3)
led.blink_twice()
