# learnedIndex
###complile and run btree
g++ runbtree.cpp -std=c++17 -I/home/z5028465/Desktop/summer/stx-btree/include -o runbtree -ftree-vectorize -march=native -Ofast -finline-functions -m64 -funroll-loops
./runbtree uniform 10000 uniform
###complile and run pgm index
g++ main.cpp -std=c++17 -I/home/z5028465/Desktop/summer/PGM-index/include -o main -ftree-vectorize -march=native -Ofast -finline-functions -m64 -funroll-loops
./main uniform 10000 uniform
###todos
1. do this on larger/real datasets
2. add rmi 
