#!/bin/bash

# Available Mixtral models by quality (best to good)
echo "Mixtral Model Options (ordered by accuracy):"
echo
echo "1. mixtral:8x7b-instruct-v0.1-fp16    (87GB) - Highest accuracy, CPU only"
echo "2. mixtral:8x7b-instruct-v0.1-q8_0    (45GB) - Excellent, CPU+GPU split"
echo "3. mixtral:8x7b-instruct-v0.1-q6_K    (34GB) - Very good, CPU+GPU split" 
echo "4. mixtral:8x7b-instruct-v0.1-q5_K_M  (30GB) - Good, CPU+GPU split"
echo "5. mixtral:8x7b-instruct-v0.1-q5_0    (28GB) - Good, mostly GPU"
echo "6. mixtral:8x7b-instruct-v0.1-q4_K_M  (26GB) - Standard, full GPU"
echo "7. mixtral:8x7b-instruct-v0.1-q4_0    (24GB) - Lower quality"
echo
