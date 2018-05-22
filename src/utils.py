#!/usr/bin/python3

import os
import subprocess

def run(input_file):
  # static version is faster
  args = ['./converter_static', input_file, '/dev/null']
  return subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def mkdir(path):
  if not os.path.isdir(path):
    os.mkdir(path)

def file_read(filename):
  with open(filename, 'rb') as file:
    return file.read()

def file_write(filename, content):
  with open(filename, 'wb') as file:
    file.write(content)

# save crash messages to keep track of duplicate
saved = {}
n_saved = 0
def save(path, input_file, code, out, duplicate=False):
  """
  We save the input file into the path given in entry, if the error type doesn't occur before.
  The code and out entries make the message describing the crash (error type).
  The duplicate entry is used to permit duplicate error files.
  It is mainly used in the generation_fuzzer because the crashes generate the same error type.
  """
  global saved, n_saved
  mess = str(code) + ': ' + str(out)
  if not duplicate and mess in saved:
    return
  saved[mess] = True
  crash_file = path + '/input_' + str(n_saved) + '.img'
  n_saved += 1
  os.rename(input_file, crash_file)
  print('crash', mess, 'saved in', crash_file)
