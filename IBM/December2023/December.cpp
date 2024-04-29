// #include <cmath>
// #include <fstream>
// #include <iostream>
// #include <map>
// #include <unordered_map>
// #include <vector>
// using namespace std;

// bool is_prime(int n) {
//   if (n <= 1)
//     return false;
//   for (int i = 2; i * i <= n; ++i) {
//     if (n % i == 0)
//       return false;
//   }
//   return true;
// }

// std::unordered_map<int, int> prime_factorization(int n) {
//   std::unordered_map<int, int> factors;
//   while (n % 2 == 0) {
//     factors[2]++;
//     n /= 2;
//   }
//   for (int i = 3; i * i <= n; i += 2) {
//     while (n % i == 0) {
//       factors[i]++;
//       n /= i;
//     }
//   }
//   if (n > 1) {
//     factors[n]++;
//   }
//   return factors;
// }

// int A364443(int n) {
//   int count = 0;
//   for (int k = n * n + 1; k <= (n + 1) * (n + 1); ++k) {
//     bool is_comp = false;
//     for (auto p : prime_factorization(k)) {
//       if (p.first % 3 == 2 && (p.second % 2 != 0)) {
//         is_comp = true;
//         break;
//       }
//     }
//     if (!is_comp) {
//       count++;
//     }
//   }
//   return --count;
// }

// void calculateAndWriteToFile(int startN, int endN, const string &filename) {
//   ofstream outputFile(filename);
//   if (!outputFile.is_open()) {
//     cerr << "Error opening file: " << filename << endl;
//     return;
//   }

//   // Calculate and write the value for the first n separately
//   long long n = startN;
//   long long result = A364443(n);
//   outputFile << n << " " << result << endl;

//   // Calculate and write the values for the remaining n values
//   for (n = startN + 1; n <= endN; ++n) {
//     result = A364443(n);
//     outputFile << n << " " << result << endl;
//   }

//   outputFile.close();
// }

// int main() {
//   // Set the range of n values and the output file name
//   int startN = 2000000;
//   int endN = 5000000;
//   string outputFilename = "output.txt";

//   // Call the function to calculate and write the values to the text file
//   calculateAndWriteToFile(startN, endN, outputFilename);

//   return 0;
// }

#include <cmath>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <vector>

using namespace std;

bool is_prime(int n, int sqrt_n) {
  if (n <= 1)
    return false;
  for (int i = 2; i <= sqrt_n; ++i) {
    if (n % i == 0)
      return false;
  }
  return true;
}

void prime_factorization(int n, std::unordered_map<int, int> &factors,
                         int sqrt_n) {
  while (n % 2 == 0) {
    factors[2]++;
    n /= 2;
  }

  for (int i = 3; i <= sqrt_n; i += 2) {
    while (n % i == 0) {
      factors[i]++;
      n /= i;
    }
  }

  if (n > 1) {
    factors[n]++;
  }
}

int A364443(int n) {
  int sqrt_n = sqrt(n);
  int count = 0;

  for (int k = n * n + 1; k <= (n + 1) * (n + 1); ++k) {
    std::unordered_map<int, int> factors;
    prime_factorization(k, factors, sqrt(k));

    bool is_comp = false;
    for (auto p : factors) {
      if (p.first % 3 == 2 && (p.second % 2 != 0)) {
        is_comp = true;
        break;
      }
    }

    if (!is_comp) {
      count++;
    }
  }

  return --count;
}

void calculateAndWriteToFile(int startN, int endN, const string &filename) {
  ofstream outputFile(filename);
  if (!outputFile.is_open()) {
    cerr << "Error opening file: " << filename << endl;
    return;
  }

  // Calculate and write the value for the first n separately
  long long n = startN;
  long long result = A364443(n);
  outputFile << n << " " << result << endl;

  // Calculate and write the values for the remaining n values
  for (n = startN + 1; n <= endN; ++n) {
    result = A364443(n);
    outputFile << n << " " << result << endl;
  }

  outputFile.close();
}

int main() {
  // Set the range of n values and the output file name
  int startN = 2000000;
  int endN = 5000000;
  string outputFilename = "output.txt";

  // Call the function to calculate and write the values to the text file
  calculateAndWriteToFile(startN, endN, outputFilename);

  return 0;
}
