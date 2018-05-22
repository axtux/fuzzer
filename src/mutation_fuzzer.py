#!/usr/bin/python3

import random

from utils import *


def fuzz_bytes(input_seed, to_randomize):
  bytes_array = bytearray(input_seed)
  bytes_to_change = random.sample(range(2, len(bytes_array)), to_randomize)
  for b in bytes_to_change:
    bytes_array[b] = random.randint(0, 255)
  return bytes_array


def fuzz_check(input_seed, max_tests, to_randomize):

  input_seed = file_read(input_seed)
  l = len(input_seed)
  print('\nInput size is', l, 'bytes')

  try:
    max_tests = int(max_tests)
    if max_tests < 1:
      usage('MAX_TESTS should be > 0')
  except ValueError:
    usage('"' + str(max_tests) + '" is not a valid integer')
  print('Running test', max_tests, 'times')

  try:
    to_randomize = round(l * float(to_randomize))
    if to_randomize < 0 or to_randomize > l:
      usage('PART_TO_RANDOMIZE should be between 0 and 1')
  except ValueError:
    usage('"' + to_randomize + '" is not a valid float')
  print('Randomizing', to_randomize, 'bytes\n')

  fuzz(input_seed, max_tests, to_randomize)


def fuzz(input_seed, max_tests, to_randomize):
  crash_file = 'crash/input_0.img'
  input_file = 'input_0.img'
  for i in range(1, max_tests + 1):
    fuzz_input = fuzz_bytes(input_seed, to_randomize)
    file_write(input_file, fuzz_input)

    result = run(input_file)
    out = result.stderr.decode('ascii').replace('\n', '. ')

    # error if '*' in stderr
    if out.find('*') != -1:
      save(input_file, result.returncode, out)


if __name__ == '__main__':
  argc = len(sys.argv)
  if argc != 4:
    usage()

  if not os.path.isdir('crash'):
    os.mkdir('crash')
  fuzz_check(sys.argv[1], sys.argv[2], sys.argv[3])

  print('\ndone')
