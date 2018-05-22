#!/usr/bin/python3

import os
import sys
import random
import subprocess

"""
	we use these variable to fit the fields that not interest us in the different function leading to a crash
"""
magic =  0xcdab.to_bytes(2,"little") #the number is 2 because 2*8 bits = 16 bits
version = 0x0064.to_bytes(2,"little")
width = 0x000002.to_bytes(4,"little")
height = 0x000002.to_bytes(4,"little")
size = 0x000002.to_bytes(4,"little") # this represents the number of colors ( size color table)

"""
 	return the table of colors fields according to the number given in parameter
"""
def color_table(nbr):
  if(nbr<1):
	  usage("the number of colors must be positive")
  table= random.randint(0,0xFFFFFFFF).to_bytes(4,"little")
  while(nbr>1):
	  table += random.randint(0,0xFFFFFFFF).to_bytes(4,"little")
	  nbr-=1
  return table

"""
	return the differents pixels in one field  according to the width and height given in parameter
"""
def pixels(w,h):
  pixels = random.randint(0,0xFF).to_bytes(1,"little")
  for p in range(w*h) :
	  pixels += random.randint(0,0xFF).to_bytes(1,"little")
  return pixels

def run(input_file):
  # static version is faster
  args = ['./converter_static', input_file, '/dev/null']
  return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def file_read(filename):
  with open(filename, 'rb') as file:
    return file.read()

def file_write(filename, content):
  with open(filename, 'wb') as file:
    file.write(content)


def usage(error=None):
  if error is not None:
    print('\n\tERROR:', error)
  print('\nusage:', sys.argv[0], 'INPUT_SEED MAX_TESTS PART_TO_RANDOMIZE')
  exit()

saved = {}

def save(input_file, code, out):
  mess = str(code) + ': ' + str(out)
  # error already saved
  if mess in saved:
    return
  saved[mess] = True
  crash_file = 'crash2/input_'+str(len(saved))+'.img'
  os.rename(input_file, crash_file)
  print('crash', mess, 'saved in', crash_file)

def fuzz(fuzz_input):
  crash_file = 'crash2/input_0.img'
  input_file = 'input_1.img'
  file_write(input_file, fuzz_input)
  result = run(input_file)
  out = result.stderr.decode('ascii').replace('\n', '. ')
  # error if '*' in stderr
  print("\n resultat obtenu du test: ",out)
  if out.find('*') != -1:
  	save(input_file, result.returncode, out)


def fuzz_magic_number():
  return ## TODO: test magic number ( brut force done without response)

"""
	This fuzzer test the number of color field.
	It must crash when the value is upper than 0x80000000
"""
def fuzz_number_colors():
  print("begin fuzz 1")
  file = magic + version + width + height # we fill the different fields with good values
  crash_number = random.randint(0x80000000,0xFFFFFFFF).to_bytes(4,"little")
  file += crash_number
  file += color_table(10)
  file += pixels(2, 2)

  fuzz(file)
  print("end fuzz 1")

if __name__ == '__main__':

  if not os.path.isdir('crash'):
    os.mkdir('crash')

  fuzz_magic_number()
  fuzz_number_colors()

  print('\ndone')
