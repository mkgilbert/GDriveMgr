#!/bin/bash
# runs all tests in this folder

cd ..
for f in tests/test*.py; do
    python $f;
done

