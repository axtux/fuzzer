#!/usr/bin/python3

import random
import utils

CRASH_PATH = 'crash2'

"""
  we use these variable to fit the fields that not interest us in the different function leading to a crash
"""
# to_bytes first parameter is length
magic = 0xcdab.to_bytes(2, "little")
version = 0x0064.to_bytes(2, "little")
width = 0x000002.to_bytes(4, "little")
height = 0x000002.to_bytes(4, "little")
size = 0x000002.to_bytes(4, "little") # number of colors (color table size)


def color_table(length):
  """
  Generate color table of length colors with random colors.
  """
  table = bytes()
  for i in range(length) :
    table += random.randint(0, 0xFFFFFFFF).to_bytes(4, "little")
  return table

def pixels(w, h):
  """
  Get pixel bytes from width and height
  """
  pixels = bytes()
  for p in range(w * h) :
    pixels += random.randint(0, 0xFF).to_bytes(1, "little")
  return pixels

def fuzz(fuzz_input):
  """
  Run the Converter on the input file and generate an output file in case of crash
  The temp_file is used as an imput to the converter
  """
  tmp_file = CRASH_PATH + '/tmp_input.img'
  utils.file_write(tmp_file, fuzz_input)
  result = utils.run(tmp_file)
  out = result.stderr.decode('ascii').replace('\n', '. ')
  # error if '*' in stderr
  if out.find('*') != -1:
    utils.save(CRASH_PATH, tmp_file, result.returncode, out, True)

def fuzz_number_colors():
  """
  This fuzzer test a crash value for the color number field.
  It must crash when the value is lower than 0x80000000 and upper than 0xFFFFFFFF.
  This is the range of negative numbers.
  """
  print("\n begin fuzz 1 \n")
  file = magic + version + width + height # we fill the different fields with good values
  crash_number = random.randint(0x80000000, 0xFFFFFFFF).to_bytes(4, "little")
  file += crash_number # we add the crash field
  file += color_table(10) + pixels(2, 2) # we add the others good fields

  fuzz(file)
  print("\n end fuzz 1 \n")

def fuzz_version():
  """
    This fuzzer test a crash value for the version field.
    It must crash when the value is between 0x36 and upper than 0x41.
  """
  print("\n begin fuzz 2 \n")
  file = magic # we fill the first field with a good value
  crash_version = random.randint(0x0036, 0x0041).to_bytes(2, "little")
  file += crash_version # we add the crash field
  file += width + height + size + color_table(10) + pixels(2, 2) # we add the others good fields

  fuzz(file)
  print("\n end fuzz 2 \n")

def fuzz_negative():
  """
    This fuzzer test crash values for the height field.
    It must crash when the height field is negative.
  """
  print("\n begin fuzz 3 \n")
  file = magic + version + width#  we fill the different fields with good values
  crash_height = random.randint(0x80000000, 0xFFFFFFFF).to_bytes(4, "little")
  file += crash_height # we add the crash field
  file += size + color_table(10) + pixels(2,2) # we add the others good fields

  fuzz(file)
  print("\n end fuzz 3 \n")

def fuzz_large():
  """
    This fuzzer test large numbers for the width and height.
	It must crash when the values are not too big, but big enough to have the too large exception .
  """
  print("\n begin fuzz 4 \n")
  file = magic + version #  we fill the different fields with good values
  crash_height = random.randint(0x0000C000, 0x0000FFFF).to_bytes(4, "little")
  crash_width = random.randint(0x0000C000, 0x0000FFFF).to_bytes(4, "little")
  file += crash_width + crash_height # we add the crash fields
  file += size + color_table(10) + pixels(2,2) # we add the others good fields

  fuzz(file)
  print("\n end fuzz 4 \n")

if __name__ == '__main__':
  utils.mkdir(CRASH_PATH)

  fuzz_number_colors()
  fuzz_version()
  fuzz_negative()
  fuzz_large()

  print('\ndone')
