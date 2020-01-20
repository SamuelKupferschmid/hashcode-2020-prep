#include<iostream>
using namespace std;

// A utility function that returns maximum of two integers  
int max(int a, int b) { return (a > b) ? a : b; }

  
int knapSack(int* val, int n, int maxV)
{
	if (maxV == 0)
		return 0;

	if (n == 0)
		return 0;

	int option1 = 0;
	if (val[n - 1] <= maxV)
		option1 = knapSack(val, n - 1, maxV - val[n - 1]) + val[n - 1];

	int option2 = knapSack(val, n - 1, maxV);

	return max(option1, option2);
	
}

// Driver code  
int main()
{
	int maxValue;
	int n;
	cin >> maxValue>>n;
	int* val = new int[n];
	for (int i = 0; i < n; i++)
		cin >> val[i];

	cout<<knapSack(val, n, maxValue);
	return 0;
}

