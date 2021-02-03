#include <vector>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include "pgm/pgm_index.hpp"

int main() {
    // Generate some random data
    std::vector<int> data(1000000);
    std::generate(data.begin(), data.end(), std::rand);
    data.push_back(56);
    std::sort(data.begin(), data.end());

    // Construct the PGM-index
    const int epsilon = 128; // space-time trade-off parameter
    pgm::PGMIndex<int, epsilon> index(data);

    // Query the PGM-index
    auto q = 56;
    auto range = index.search(q);
    auto lo = data.begin() + range.lo;
    auto hi = data.begin() + range.hi;
    std::cout << range.pos <<std::endl;

    return 0;
}
