#include <resource_retriever/retriever.hpp>
#include <iostream>
int main(int argc, char** argv) {
  for (int i=1; i<argc; ++i) {
    try {
      resource_retriever::Retriever r;
      auto mem = r.get(argv[i]);
      std::cout << argv[i] << " -> OK size=" << mem.size << std::endl;
    } catch (const std::exception& e) {
      std::cout << argv[i] << " -> FAIL " << e.what() << std::endl;
    }
  }
  return 0;
}
