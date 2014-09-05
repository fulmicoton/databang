#!/bin/bash

rm -f prediction.zip result.txt make.log
cd sandbox && make &> make.log 
