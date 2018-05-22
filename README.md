# Mutation based fuzzer
Usage
```bash
$ ./src/mutation_fuzzer.py INPUT_FILE N_TESTS PART_TO_RANDOMIZE
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

Usage
```bash
$ ./src/generation_fuzzer.py
```

For this part, we have implemented 4 functions that always crash the Converter. The values chosen for these crashing have been found by testing multiple possibilities first. As for the previous fuzzer, we generate a new file at each function and do the same manipulations.

# Release

The output files given by the crashes are stored in the crash files folder.
The files are numbered from 0 to 3, each one correspond to the function called in the main of the file. Each one is well described by his documentation.
