# Mutation based fuzzer
Usage
```bash
$ ./src/mutation_based.py INPUT_FILE N_TESTS PART_TO_RANDOMIZE
```

Arguments :
- `INPUT_FILE` input file to change randomly
- `N_TESTS` maximum number of tests to run
- `PART_TO_RANDOMIZE` part of file to randomize (between 0 and 1)

Run N_TESTS tests. For each test, INPUT_FILE is read. Some bytes (depending on
PART_TO_RANDOMIZE) are randomly changed and a new file is generated. This file
is given to the converter as input file. If this file crashes the converter, a
message is shown containing converter return code, converter error message and
filename where this input file has been saved.

# Generation based fuzzer

TODO
