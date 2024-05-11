#!/bin/bash

# Compile C++ code
g++ -o output "$1"

# Run compiled code with input from input.txt and output to output.txt
./output < input.txt > output.txt

