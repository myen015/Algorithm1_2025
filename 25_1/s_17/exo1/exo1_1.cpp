#include <bits/stdc++.h>
using namespace std;

const int MAX = 200'007;
const int MOD = 1'000'000'007;

int findOne(vector<int> &v, int l, int r){
	if(l == r){
		return l;
	}
	int m = l + (r - l) / 2;
	
	int sumL = 0;
	for(int i = l; i <= m; i++){
		sumL += v[i];
	}
	if(sumL > 0){
		return findOne(v, l, m);
	} else {
		return findOne(v, m + 1, r);
	}
}

void solve() {
	int n;
	cin >> n;
	vector<int> v(n);
	for(int i = 0; i < v.size(); i++){
		cin >> v[i];
	}
	cout <<findOne(v, 0, v.size() - 1);
}
int main(){
	int t = 1;
	while(t--){
		solve();
	}
}

	