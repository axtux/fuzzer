#!/usr/bin/python3

import sys
import os
import subprocess

saved = {} # crash messages saved for the first fuzzer
crashes = {}# crash messages for the second fuzzer

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


def save(input_file, code, out, duplicate=True):
  mess = str(code) + ': ' + str(out)
  if duplicate :
    # error already saved
    if mess in saved:
      return
    saved[mess] = True
    crash_file = 'crash2/input_'+str(len(saved))+'.img'
    os.rename(input_file, crash_file)
    print('crash', mess, 'saved in', crash_file)

  else : # We know we have 4 different type of crash
    crash_file = 'crash2/input_'+str(len(crashes))+'.img'
    crashes[mess] = crash_file
    os.rename(input_file, crash_file)
    print('crash', mess, 'saved in', crash_file)
