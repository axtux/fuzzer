#!/usr/bin/python3

import random
import utils

CRASH_PATH = 'crash2'

"""
  we use these variable to fit the fields that not interest us in the different function leading to a crash
  These values depends on the system you are, in my case my system works in big endian.
  It may not work if your system is little endian, in this case change the values here under
"""
# to_bytes first parameter is length
magic = 0xcdab.to_bytes(2, "little")
version = 0x0064.to_bytes(2, "little")
width = 0x000002.to_bytes(4, "little")
height = 0x000002.to_bytes(4, "little")
# number of colors (color table size)
size = 0x000002.to_bytes(4, "little")


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
  pixels = random.randint(0, 0xFF).to_bytes(1, "little")
  for p in range(w * h) :
    pixels += random.randint(0, 0xFF).to_bytes(1, "little")
  return pixels


def fuzz(fuzz_input):
  tmp_file = CRASH_PATH + '/tmp_input.img'
  utils.file_write(tmp_file, fuzz_input)
  result = utils.run(tmp_file)
  out = result.stderr.decode('ascii').replace('\n', '. ')
  # error if '*' in stderr
  print("\n resultat obtenu du test: ", out)
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
  crash_number = random.randint(0x36, 0x41).to_bytes(2, "little")
  file += crash_number # we add the crash field
  file += width + height + size + color_table(10) + pixels(2, 2) # we add the others good fields

  fuzz(file)
  print("\n end fuzz 2 \n")


if __name__ == '__main__':
  utils.mkdir(CRASH_PATH)

  fuzz_number_colors()
  fuzz_version()

  print('\ndone')
