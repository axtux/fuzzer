#!/usr/bin/python3

import sys
import random

import utils

CRASH_PATH = 'crash'


def fuzz_bytes(input_seed, n_bytes):
  """
  Randomize n_bytes bytes of input_seed and return result
  """
  bytes_array = bytearray(input_seed)
  bytes_to_change = random.sample(range(len(bytes_array)), n_bytes)
  for b in bytes_to_change:
    bytes_array[b] = random.randint(0, 255)
  return bytes_array


def fuzz_check(input_file, n_tests, to_randomize):
  """
  Check user inputs and process them as required by fuzz
  """
  input_seed = utils.file_read(input_file)
  l = len(input_seed)
  print('\nInput size is', l, 'bytes')

  try:
    n_tests = int(n_tests)
    if n_tests < 1:
      usage('N_TESTS should be > 0')
  except ValueError:
    usage('"' + str(n_tests) + '" is not a valid integer')
  print('Running test', n_tests, 'times')

  try:
    n_bytes = round(l * float(to_randomize))
    if n_bytes < 0 or n_bytes > l:
      usage('PART_TO_RANDOMIZE should be between 0 and 1')
  except ValueError:
    usage('"' + to_randomize + '" is not a valid float')
  print('Randomizing', n_bytes, 'bytes\n')

  return input_seed, n_tests, n_bytes


def fuzz(input_seed, n_tests, n_bytes):
  """
  Run n_tests tests on converter. For each test, randomize n_bytes bytes of
  input_seed and write it to a temporary file. Then, converter is run with
  temporary file as input. If this file makes the converter crash, it is saved
  to CRASH_PATH directory.
  """
  tmp_file = CRASH_PATH + '/tmp_input.img'
  for i in range(n_tests):
    fuzz_input = fuzz_bytes(input_seed, n_bytes)
    utils.file_write(tmp_file, fuzz_input)

    result = utils.run(tmp_file)
    out = result.stderr.decode('ascii').replace('\n', '. ')

    # error if '*' in output
    if out.find('*') != -1:
      utils.save(CRASH_PATH, tmp_file, result.returncode, out)


def usage(error=None):
  """
  Print usage with eventual error message.
  """
  if error is not None:
    print('\n\tERROR:', error)
  print('\nusage:', sys.argv[0], 'INPUT_SEED MAX_TESTS PART_TO_RANDOMIZE')
  exit()


if __name__ == '__main__':
  argc = len(sys.argv)
  if argc != 4:
    usage()

  utils.mkdir(CRASH_PATH)
  input_seed, n_tests, n_bytes = fuzz_check(sys.argv[1], sys.argv[2], sys.argv[3])
  fuzz(input_seed, n_tests, n_bytes)

  print('\ndone')
