# learnedIndex
### complile and run btree
```sh
g++ runbtree.cpp -std=c++17 -I/home/z5028465/Desktop/summer/stx-btree/include -o runbtree -ftree-vectorize -march=native -Ofast -finline-functions -m64 -funroll-loops
./runbtree uniform 10000 uniform
```
### complile and run pgm index
```sh
g++ main.cpp -std=c++17 -I/home/z5028465/Desktop/summer/PGM-index/include -o main -ftree-vectorize -march=native -Ofast -finline-functions -m64 -funroll-loops
./main uniform 10000 uniform
```
### todos
- do this on larger/real datasets
- add rmi
