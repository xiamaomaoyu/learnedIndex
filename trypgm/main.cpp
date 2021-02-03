#include <vector>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include "pgm/pgm_index.hpp"
#include <fstream>
#include <sstream>

std::vector<int> load_data(){
  std::vector<int> data;
  std::string myText;
  std::ifstream MyReadFile("1dExample.csv");
  // Use a while loop together with the getline() function to read the file line by line
  while (getline (MyReadFile, myText)) {
    // Output the text from the file
    data.push_back(std::stoi(myText));
  }
  // Close the file
  MyReadFile.close();
  return data;
}

struct range{
   int min;
   int max;
};

std::vector<range> load_queries(){
  std::vector<range> queries;
  std::string myText;
  std::ifstream MyReadFile("1dQueriesExample.csv");
  // Use a while loop together with the getline() function to read the file line by line
  while (getline (MyReadFile, myText)) {
    // Output the text from the file
    std::stringstream check1(myText);
    std::string text;
    range q;
    getline(check1, text, ',');
    q.min = std::stoi(text);
    getline(check1, text, ',');
    q.max = std::stoi(text);
    queries.push_back(q);
  }
  // Close the file
  MyReadFile.close();
  return queries;

}





int main() {

    auto data = load_data();
    auto queries = load_queries();
    // Construct the PGM-index
    const int epsilon = 128; // space-time trade-off parameter
    pgm::PGMIndex<int, epsilon> index(data);
    for (auto & query : queries) {
      auto up_range = index.search(query.max);
      auto up_lo = data.begin() + up_range.lo;
      auto up_hi = data.begin() + up_range.hi;
      auto max = *std::lower_bound(up_lo, up_hi, query.max);
      auto lo_range = index.search(query.min);
      auto lo_lo = data.begin() + lo_range.lo;
      auto lo_hi = data.begin() + lo_range.hi;
      auto min = *std::lower_bound(lo_lo, lo_hi, query.min);
      range result{min ,max};
      std::cout << result.min << ' ' << result.max << std::endl;
    }


    return 0;
}
