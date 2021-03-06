#include <vector>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <fstream>
#include <sstream>
#include "stx/btree_map.h"
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




int main(int argc, char *argv[]) {

    std::string distribution = argv[1];
    std::string volume = argv[2];
    std::string query_type = argv[3];
    std::string data_filename = distribution + volume + ".csv";
    std::string query_filename = query_type+'-'+distribution+"10000"+".csv";
    std::string data_dirname = "/home/z5028465/Desktop/summer/data/1d/data/";
    std::string query_dirname = "/home/z5028465/Desktop/summer/data/1d/query/";

    // std::string data_filename = "1dExample.csv";
    // std::string query_filename = "1dQueriesExample.csv";
    // std::string data_dirname = "/home/z5028465/Desktop/summer/learnedIndex/";
    // std::string query_dirname = "/home/z5028465/Desktop/summer/learnedIndex/";

    auto data = load_data(data_filename,data_dirname);
    auto queries = load_point_query(query_filename,query_dirname);

    typedef stx::btree_map<int, std::string> btree_type;
    unsigned int numkeys = data.size();
    std::vector<std::pair<int, std::string> > pairs(numkeys);
    for (unsigned int i = 0; i < numkeys; i++)
    {
        pairs[i].first = data[i];
        pairs[i].second = "key";
    }

    std::sort(pairs.begin(), pairs.end());
    btree_type bt;
    bt.bulk_load(pairs.begin(), pairs.end());

    std::clock_t begin = clock();
    for (auto & query : queries) {
      auto result = bt.lower_bound(query);
      // auto min = bt.upper_bound(query.min);
      // auto max = bt.lower_bound(query.max);
    }
    std::clock_t end = clock();
    std::cout << "query time: " << float(end-begin)/CLOCKS_PER_SEC << "ms. " << std::endl;

}
