#include <iostream>
#include <cstring>
#include <vector>
#include <set>
   
template <typename Iterator, typename Predicate>
Iterator mymax(Iterator first, Iterator last, Predicate pred) {
   if (first == last)
      return last;

   Iterator max_element = first;
   for (Iterator it = first; it != last; ++it) {
      if (pred(*it, *max_element)) {
         max_element = it;
      }
   }
   return max_element;
}

template <typename T>
bool gt(const T& a, const T& b) {
   return a > b;
}

bool gt_str(const char* a, const char* b) {
   return std::strcmp(a, b) > 0;
}

int main() {
   int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
   char arr_char[] = "Suncana strana ulice";
   const char* arr_str[] = {
      "Gle", "malu", "vocku", "poslije", "kise",
      "Puna", "je", "kapi", "pa", "ih", "njise"
   };

   const int* max_int = mymax(std::begin(arr_int), std::end(arr_int), gt<int>);
   std::cout << "max_int = " << *max_int << std::endl;

   const char* max_char = mymax(std::begin(arr_char), std::end(arr_char) - 1, gt<char>);
   std::cout << "max_char = " << *max_char << std::endl;

   const char** max_str = mymax(std::begin(arr_str), std::end(arr_str), gt_str);
   std::cout << "max_str = " << *max_str << std::endl;

   std::vector<int> vec_int = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
   auto max_vec_int = mymax(vec_int.begin(), vec_int.end(), gt<int>);
   std::cout << "max_vec_int = " << *max_vec_int << std::endl;

   std::set<double> set_double = { 3.5, 1.2, 6.7, 4.8, 2.3 };
   auto max_set_double = mymax(set_double.begin(), set_double.end(), gt<double>);
   std::cout << "max_set_double = " << *max_set_double << std::endl;

   return 0;
}