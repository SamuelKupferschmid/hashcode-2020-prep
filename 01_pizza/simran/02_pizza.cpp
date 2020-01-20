#include<iostream>
using namespace std;

// A utility function that returns maximum of two integers  
int max(int a, int b) { return (a > b) ? a : b; }


int knapSack(int* val, int n, int maxV,int** dp)
{
	if (maxV == 0)
		return 0;

	if (n == 0)
		return 0;

	if (dp[n][maxV] >= 0)
	{
		return dp[n][maxV];

	}


	int option1 = 0;
	if (val[n - 1] <= maxV)
		option1 = knapSack(val, n - 1, maxV - val[n - 1],dp) + val[n - 1];

	int option2 = knapSack(val, n - 1, maxV,dp);

	dp[n][maxV] = max(option1, option2);

	return dp[n][maxV];

}

// Driver code  
int main()
{
	int maxValue;
	int n;
	cin >> maxValue >> n;
	int* val = new int[n];
	for (int i = 0; i < n; i++)
		cin >> val[i];

	int** dp = new int*[n + 1];

	for(int i=0;i<=n;i++)
	{
	dp[i]= new int[maxValue+1];
		for(int j=0;j<=maxValue;j++)
			dp[i][j]=-1;
	}

	cout << knapSack(val, n, maxValue, dp);
	return 0;
}
