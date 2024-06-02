all:
	g++ -std=c++20 -O3 -march=native -Wall -I/usr/local/include/eigen3/ kdtree.cpp main.cpp -o matcher