#include <bits/stdc++.h>
using namespace std;
int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n=4, W=5;
    vector<int> wt={2,3,4,5};
    vector<int> val={3,4,5,6};
    vector<int> dp(W+1,0);

    for(int i=0;i<n;i++){
        for(int w=W;w>=wt[i];w--){
            dp[w]=max(dp[w],dp[w-wt[i]]+val[i]);
        }
    }

    cout<<dp[W];
    return 0;
}
