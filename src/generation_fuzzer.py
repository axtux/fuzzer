#!/usr/bin/python3

import random
from utils import *

CRASH_PATH = 'crash2'

"""
	we use these variable to fit the fields that not interest us in the different function leading to a crash
	These values depends on the system you are, in my case my system works in big endian.
	It may not work if your system is little endian, in this case change the values here under
"""
magic = 0xcdab.to_bytes(2, "little") # the number is 2 because 2*8 bits = 16 bits
version = 0x0064.to_bytes(2, "little")
width = 0x000002.to_bytes(4, "little")
height = 0x000002.to_bytes(4, "little")
size = 0x000002.to_bytes(4, "little") # this represents the number of colors ( size color table)
# # TODO: https://stackoverflow.com/questions/1400012/endianness-of-integers-in-python

"""
 	return the table of colors fields according to the number given in parameter
"""


def color_table(nbr):
  if nbr < 1 :
	  usage("the number of colors must be positive")
  table = random.randint(0, 0xFFFFFFFF).to_bytes(4, "little")
  while nbr > 1 :
	  table += random.randint(0, 0xFFFFFFFF).to_bytes(4, "little")
	  nbr -= 1
  return table


"""
	return the differents pixels in one field  according to the width and height given in parameter
"""


def pixels(w, h):
  pixels = random.randint(0, 0xFF).to_bytes(1, "little")
  for p in range(w * h) :
	  pixels += random.randint(0, 0xFF).to_bytes(1, "little")
  return pixels


def fuzz(fuzz_input):
  crash_file = CRASH_PATH + '/input_0.img'
  input_file = 'input_1.img'
  file_write(input_file, fuzz_input)
  result = run(input_file)
  out = result.stderr.decode('ascii').replace('\n', '. ')
  # error if '*' in stderr
  print("\n resultat obtenu du test: ", out)
  if out.find('*') != -1:
    save(CRASH_PATH, input_file, result.returncode, out, True)


"""
	This fuzzer test a crash value for the color number field.
	It must crash when the value is lower than 0x80000000 and upper than 0xFFFFFFFF.
	This is the range of negative numbers.
"""


def fuzz_number_colors():
  print("\n begin fuzz 1 \n")
  file = magic + version + width + height # we fill the different fields with good values
  crash_number = random.randint(0x80000000, 0xFFFFFFFF).to_bytes(4, "little")
  file += crash_number # we add the crash field
  file += color_table(10) + pixels(2, 2) # we add the others good fields

  fuzz(file)
  print("\n end fuzz 1 \n")


"""
	This fuzzer test a crash value for the version field.
	It must crash when the value is between 0x36 and upper than 0x41.
"""


def fuzz_version():
  print("\n begin fuzz 2 \n")
  file = magic # we fill the first field with a good value
  crash_number = random.randint(0x36, 0x41).to_bytes(2, "little")
  file += crash_number # we add the crash field
  file += width + height + size + color_table(10) + pixels(2, 2) # we add the others good fields

  fuzz(file)
  print("\n end fuzz 2 \n")


if __name__ == '__main__':

  if not os.path.isdir(CRASH_PATH):
    os.mkdir(CRASH_PATH)

  fuzz_number_colors()
  fuzz_version()

  print('\ndone')
