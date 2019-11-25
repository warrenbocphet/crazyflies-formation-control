import time
from threading import Timer

def print_me(number):
	print(number)
	number = number + 1
	Timer(1,print_me, args=[number]).start()


print_me(1)

