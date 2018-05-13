#!/usr/bin/python3

import os
import sys
import random
import subprocess

def run(input_file):
  # static version is faster
  args = ['./converter_static', input_file, '/dev/null']
  # disable closing descriptor/restore signals for performance
  return subprocess.Popen(args, stderr=subprocess.PIPE, bufsize=4096, close_fds=False, restore_signals=False)

def file_read(filename):
  with open(filename, 'rb') as file:
    return bytearray(file.read())

def file_write(filename, content):
  with open(filename, 'wb') as file:
    file.write(content)

def fuzz_bytes(input, to_randomize):
  bytes_to_change = random.sample(range(len(input)), to_randomize)
  for b in bytes_to_change:
    input[b] = random.randint(0, 255)
  return input

def fuzz_check(input_seed, max_tests, to_randomize):
  
  input_seed = file_read(input_seed)
  l = len(input_seed)
  print('\nInput size is', l, 'bytes')
  
  try:
    max_tests = int(max_tests)
    if max_tests < 1:
      usage('MAX_TESTS should be > 0')
  except ValueError:
    usage('"'+str(max_tests)+'" is not a valid integer')
  print('Running test', max_tests, 'times')
  
  try:
    to_randomize = round(l*float(to_randomize))
    if to_randomize < 0 or to_randomize > l:
      usage('PART_TO_RANDOMIZE should be between included 0 and included 1')
  except ValueError:
    usage('"'+to_randomize+'" is not a valid float')
  print('Randomizing', to_randomize, 'bytes\n')
  
  fuzz(input_seed, max_tests, to_randomize)

def fuzz(input_seed, max_tests, to_randomize):
  for i in range(1, max_tests+1):
    fuzz_input = fuzz_bytes(input_seed, to_randomize)
    input_file = 'input_0.img'
    file_write(input_file, fuzz_input)

    result = run(input_file)
    out = str(result.stderr)
    code = result.returncode
    error = out.find('*') != -1
    
    if error:
      while os.path.isfile('crash/'+input_file):
        input_file = 'input_'+str(random.randint(0, 1e6))+'.img'
      os.rename(input_file, 'crash/'+input_file)
      print('test', i, 'crashing, saved in', input_file)

def usage(error=None):
  if error is not None:
    print('\n\tERROR:', error)
  print('\nusage:', sys.argv[0], 'INPUT_SEED MAX_TESTS PART_TO_RANDOMIZE')
  exit()

if __name__ == '__main__':
  argc = len(sys.argv)
  if argc != 4:
    usage()
  
  fuzz_check(sys.argv[1], sys.argv[2], sys.argv[3])
  
  print('\ndone')
