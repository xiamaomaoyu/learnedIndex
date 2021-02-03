#include <vector>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <stx/btree_map.h>
#include <stx/btree_multimap.h>

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




int main(){
    auto data = load_data();
    auto queries = load_queries();
    std::cout<<"queries loaded"<<std::endl;
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
    std::cout<<"tree constructed"<<std::endl;

    for (auto & query : queries) {
      auto max = bt.lower_bound(query.max);
      auto min = bt.lower_bound(query.min);
      if( min != bt.end() && max != bt.end()){
        std::cout << min->first << ' ' << max->first << std::endl;
      }else{
        std::cout << 'Q' << query.min << ' ' << query.max<< std::endl;
      }
    }

}
