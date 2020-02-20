#include<iostream>
#include<vector>
#include <assert.h>
#include<algorithm>
#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <ostream>
#define OUT_FOLDER "..\\output\\"
#define IN_FOLDER "..\\input\\"
#define LOG(x) cout << (x) << endl
using namespace std;

string inputFolder;
string outputFolder;
string inputPath;
string outputPath;
string fileName;
ofstream outputFile;
ifstream inputFile;

string getFileName(char letter)
{
	string name;
	switch (letter) {
	case 'a': name = "a_example"; break;
	case 'b': name = "b_small"; break;
	case 'c': name = "c_medium"; break;
	case 'd': name = "d_quite_big"; break;
	case 'e': name = "e_also_big"; break;
	default:break;
	}
	fileName = name;
	return name;
}

void readInputFile()
{
	char letter;


	cout << endl << "Select input file (only first letter) -> ";
	cin >> letter;
	cout << "Path of the input folder -> ";
	cin >> inputFolder;
	cout << "Path of the output folder -> ";
	cin >> outputFolder;

	if (inputFolder == "0") inputFolder = IN_FOLDER;
	if (outputFolder == "0") outputFolder = OUT_FOLDER;

	fileName = getFileName(letter);

	inputPath = inputFolder + fileName + ".in";

	int processed = 0;
	inputFile.open(inputPath);
	if (!inputFile.is_open())
	{
		LOG("!!! FILE NOT FOUND !!!");
		throw uncaught_exception;
	}

}
void writeOutputFile(vector<int>& output)
{
	outputPath = outputFolder + fileName + ".out";
	outputFile.open(outputPath);
	if (!outputFile.is_open())
	{
		LOG("!!! FILE NOT FOUND !!!");
		throw uncaught_exception;
	}

	sort(output.begin(), output.end());
	outputFile << (int)output.size() << endl;
	for (int x : output) {
		outputFile << x << "\t";
	}
	outputFile << endl;
	outputFile.close();
}

struct pizza {
	int id, slice;
};

//void setUsedFalse(vector<pizza>& v) {
//  for (int i = 0; i < v.size(); ++i)v[i].used = false;
//}
//
//void setUsedTrue(vector<pizza>& v, int o) {
//  for (int i = 0; i < o; ++i)v[i].used = true;
//}

void copyToAns(vector<int>& a, vector<pizza>& v, int l, int r) {
	a.clear();
	a.resize(r - l);
	for (int i = l; i < r; ++i) {
		a[i - l] = v[i].id;
	}
}

int main()
{
	int n, m, i, j, q, p, score = 0;
	vector<pizza> pizzas;
	vector<int> ans;
	readInputFile();
	inputFile >> m >> n;
	pizzas.resize(n);
	for (i = 0; i < n; ++i) {
		inputFile >> pizzas[i].slice;
		pizzas[i].id = i;
	}//sort(pizza.begin(), pizza.end());
	//first check can you do all
	long long sum = 0;
	for (i = 0; i < n; ++i) {
		sum += pizzas[i].slice;
	}
	if (sum <= (long long)m) {
		// use all
		ans.resize(n);
		for (i = 0; i < n; ++i) {
			ans[i] = i;
		}
		writeOutputFile(ans);
		return 0;
	}

	for (i = 0; i < 50; ++i) {
		random_shuffle(pizzas.begin(), pizzas.end());

		int sum = 0;
		for (j = 0; sum <= m; ++j) {
			sum += pizzas[j].slice;
		}
		int l = j;
		int k;
		int over = sum - m;

		for (k = 0; k < 200; ++k) {
			int subtract = 0;
			random_shuffle(pizzas.begin(), pizzas.begin() + l);

			for (j = 0; j < l; ++j) {
				subtract += pizzas[j].slice;
				if (subtract >= over) {
					int temp = sum - subtract;
					if (temp > score) {
						score = temp;
						copyToAns(ans, pizzas, j + 1, l);
						break;
					}
				}
			}
		}
		// i will random shuffle this too because it is
	}

	writeOutputFile(ans);
	LOG(score);
}