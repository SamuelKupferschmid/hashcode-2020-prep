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


int main()
{
	
	

	//writeOutputFile(ans);
	//LOG(score);
}