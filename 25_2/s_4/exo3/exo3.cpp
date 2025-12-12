#include <bits/stdc++.h>
using namespace std;

long long fib_matrix(long long n) {
    if (n==0) return 0;
    long long F[2][2]={{1,1},{1,0}}, M[2][2]={{1,1},{1,0}};
    auto mult=[&](long long A[2][2], long long B[2][2]){
        long long x=A[0][0]*B[0][0]+A[0][1]*B[1][0];
        long long y=A[0][0]*B[0][1]+A[0][1]*B[1][1];
        long long z=A[1][0]*B[0][0]+A[1][1]*B[1][0];
        long long w=A[1][0]*B[0][1]+A[1][1]*B[1][1];
        A[0][0]=x;A[0][1]=y;A[1][0]=z;A[1][1]=w;
    };
    function<void(long long[2][2], long long)> power=[&](long long A[2][2], long long n){
        if (n==0||n==1) return;
        long long B[2][2]={{1,1},{1,0}};
        power(A,n/2); mult(A,A);
        if (n%2!=0) mult(A,B);
    };
    power(F,n-1);
    return F[0][0];
}

void fib_console_plot() {
    cout<<"\n===== Fibonacci Numbers (Matrix Exponentiation) =====\n";
    vector<long long> ns, vals;
    for(int i=0;i<=20;i++){ ns.push_back(i); vals.push_back(fib_matrix(i)); }
    long long maxv=*max_element(vals.begin(),vals.end());
    for(int i=0;i<vals.size();i++){
        int bars=(int)(50.0*vals[i]/maxv);
        cout<<setw(2)<<ns[i]<<" | "<<string(bars,'#')<<" ("<<vals[i]<<")\n";
    }
    cout<<"=====================================================\n";
    cout<<"Testing performance (rough timing):\n";
    for(int n=100;n<=1000;n+=300){
        auto t1=chrono::high_resolution_clock::now();
        fib_matrix(n);
        auto t2=chrono::high_resolution_clock::now();
        double dt=chrono::duration<double>(t2-t1).count();
        cout<<"n="<<setw(4)<<n<<"  time≈"<<dt*1e6<<" µs\n";
    }
    cout<<"Expected complexity: O(log n)\n";
}

void knapsack_console() {
    cout<<"\n===== 0/1 Knapsack (Dynamic Programming) =====\n";
    vector<int> values = {60, 100, 120};
    vector<int> weights = {10, 20, 30};
    int W = 50;
    int n = values.size();
    cout<<"Dataset:\n";
    for(int i=0;i<n;i++)
        cout<<"Item "<<i+1<<": weight="<<weights[i]<<", value="<<values[i]<<"\n";
    cout<<"Max capacity = "<<W<<"\n\n";
    vector<vector<int>> dp(n+1, vector<int>(W+1,0));
    for(int i=1;i<=n;i++)
        for(int wt=0;wt<=W;wt++)
            if(weights[i-1]<=wt)
                dp[i][wt]=max(dp[i-1][wt],dp[i-1][wt-weights[i-1]]+values[i-1]);
            else dp[i][wt]=dp[i-1][wt];
    vector<int> chosen;
    int w=W;
    for(int i=n;i>0;i--){
        if(dp[i][w]!=dp[i-1][w]){
            chosen.push_back(i);
            w-=weights[i-1];
        }
    }
    reverse(chosen.begin(),chosen.end());
    cout<<"Value distribution by capacity:\n";
    int maxv=*max_element(dp[n].begin(),dp[n].end());
    for(int i=0;i<=W;i++){
        int bars=(int)(50.0*dp[n][i]/maxv);
        cout<<setw(2)<<i<<" | "<<string(bars,'*')<<" ("<<dp[n][i]<<")\n";
    }
    cout<<"Maximum achievable value: "<<dp[n][W]<<"\n";
    cout<<"Items chosen: ";
    for(int i:chosen) cout<<i<<" ";
    cout<<"\n==============================================\n";
}

double cosine_sim(const vector<int>&x,const vector<int>&y){
    double dot=0,nx=0,ny=0;
    for(int i=0;i<x.size();i++){dot+=x[i]*y[i];nx+=x[i];ny+=y[i];}
    return dot/(nx*ny+1e-9);
}

double jaccard_sim(const vector<int>&x,const vector<int>&y){
    double inter=0,uni=0;
    for(int i=0;i<x.size();i++){inter+=x[i]&y[i];uni+=x[i]|y[i];}
    return inter/(uni+1e-9);
}

void neuro_console() {
    cout<<"\n===== Neuro Computing (Binary Vector Similarity) =====\n";
    vector<int> Ns={50,200,1000};
    mt19937 rng(time(0));
    auto hist=[&](vector<double>&arr){
        vector<int> bins(10,0);
        for(double x:arr){
            int b=min(9,(int)(x*10));
            bins[b]++;
        }
        for(int i=0;i<10;i++){
            int bars=bins[i]/5;
            cout<<fixed<<setprecision(1)<<i/10.0<<"-"<<(i+1)/10.0<<" | "<<string(bars,'#')<<" ("<<bins[i]<<")\n";
        }
    };
    for(int N:Ns){
        cout<<"\n--- Vector length N="<<N<<" ---\n";
        int samples=100;
        vector<vector<int>> data(samples, vector<int>(N));
        for(auto&v:data) for(auto&x:v) x=rng()%2;
        vector<double> sims, jaccs;
        for(int i=0;i<samples;i++)
            for(int j=i+1;j<samples;j++){
                sims.push_back(cosine_sim(data[i],data[j]));
                jaccs.push_back(jaccard_sim(data[i],data[j]));
            }
        double mean_c=accumulate(sims.begin(),sims.end(),0.0)/sims.size();
        double mean_j=accumulate(jaccs.begin(),jaccs.end(),0.0)/jaccs.size();
        cout<<"Cosine Similarity Distribution:\n"; hist(sims);
        cout<<"Jaccard Similarity Distribution:\n"; hist(jaccs);
        cout<<"Mean Cosine="<<mean_c<<"  Mean Jaccard="<<mean_j<<"\n";
    }
    int N_sparse=2000,w=5;
    double count=0;
    for(int i=1;i<=w;i++) count+=log10((double)(N_sparse-i+1)/i);
    cout<<"\nSparse vector case: N=2000, w=5\n";
    cout<<"log10(#combinations) ≈ "<<count<<"\n";
    cout<<"=====================================================\n";
}

int main(){
    while(true){
        cout<<"\n=========== Algorithm Menu ===========\n";
        cout<<"1 - Fibonacci (Matrix Exponentiation)\n";
        cout<<"2 - 0/1 Knapsack (Predefined Dataset)\n";
        cout<<"3 - Neuro Computing (Automated Tests)\n";
        cout<<"0 - Exit\n";
        cout<<"=====================================\n";
        cout<<"Select option: ";
        int c;cin>>c;
        if(c==1) fib_console_plot();
        else if(c==2) knapsack_console();
        else if(c==3) neuro_console();
        else if(c==0){ cout<<"Exiting...\n"; break; }
        else cout<<"Invalid choice\n";
    }
}