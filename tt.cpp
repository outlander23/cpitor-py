#include "bits/stdc++.h"
using namespace std;

int main() {
  vector<int> a = {1, 2, 3, 4, 5, 111, 2};
  sort(a.begin(), a.end());
  for (auto x : a)
    cout << x << " ";
}