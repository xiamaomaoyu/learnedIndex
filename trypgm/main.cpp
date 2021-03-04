#include <vector>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include "pgm/pgm_index.hpp"
#include <fstream>
#include <sstream>
#include <ctime>

std::vector<int> load_data(std::string filename, std::string dirname){
  std::vector<int> data;
  std::string myText;
  std::ifstream MyReadFile(dirname+filename);
  // Use a while loop together with the getline() function to read the file line by line
  while (getline (MyReadFile, myText)) {
    // Output the text from the file
    data.push_back(std::stoi(myText));
  }
  // Close the file
  MyReadFile.close();
  return data;
}

std::vector<int> load_point_query(std::string filename, std::string dirname){
  std::vector<int> data;
  std::string myText;
  std::ifstream MyReadFile(dirname+filename);
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

std::vector<range> load_range_query(std::string filename, std::string dirname){
  std::vector<range> queries;
  std::string myText;

  std::ifstream MyReadFile(dirname+filename);
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


int point_query(int query,auto index, std::vector<int>&  data){
  auto range = index.search(query);
  auto lo = data.begin() + range.lo;
  auto hi = data.begin() + range.hi;
  auto result = *std::lower_bound(lo, hi, query);
  return result;
}


range range_query(range query,auto index,std::vector<int>&  data){
  auto max = point_query(query.max,index,data);
  auto min = point_query(query.min,index,data);
  return {min ,max};
}



int main(int argc, char *argv[]) {

    // std::string distribution = argv[1];
    // std::string volume = argv[2];
    // std::string query_type = argv[3];
    // std::string data_filename = distribution + volume + ".csv";
    // std::string query_filename = query_type+'-'+distribution+"10000"+".csv";
    // std::string data_dirname = "/home/z5028465/Desktop/summer/data/1d/data/";
    // std::string query_dirname = "/home/z5028465/Desktop/summer/data/1d/query/";

    std::string data_filename = "1dExample.csv";
    std::string query_filename = "1dQueriesExample.csv";
    std::string data_dirname = "/home/z5028465/Desktop/summer/learnedIndex/";
    std::string query_dirname = "/home/z5028465/Desktop/summer/learnedIndex/";

    auto data = load_data(data_filename,data_dirname);
    auto queries = load_range_query(query_filename,query_dirname);
    // Construct the PGM-index
    const int epsilon = 512; // space-time trade-off parameter
    pgm::PGMIndex<int, epsilon,1> index(data);
    std::cout<<index.height()<<std::endl;
    std::clock_t begin = clock();
    for (auto & query : queries) {
      auto result = range_query(query,index,data);
      // std::cout<< query.min << ' ' << result.min << std::endl;
      // std::cout<< query.max << ' ' << result.max << std::endl;

    }
    std::clock_t end = clock();

    std::cout << "query time: " << float(end-begin)/CLOCKS_PER_SEC << "ms. " << std::endl;
    return 0;
}
