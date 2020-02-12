#include <string>
#include <iostream>
#include <map>
#include <cassert>
#include <cstdlib>
#include <cstdio>
#include <vector>
#include <set>
#include <tuple>
#include <algorithm>
#include <fstream>
#define LOG(x) cout << (x) << endl
#define OUT_FOLDER "..\\output\\"
#define IN_FOLDER "..\\input\\"
using namespace std;
string outputPath;
string outputFolder;
string fileName;

struct connection
{
	int cache, latency,result;
};

struct request
{
	int from, video,video_size,count;
};

struct endpoint
{
	int base_latency;
	vector<connection> conn;
	vector<request> requests;
};



int n_videos, n_endpoints, n_caches, cache_size, n_requests;;
vector<int> video_size;
vector<endpoint> endpoints;
vector<request> requests;

string getFileName(char letter)
{
	string name;
	switch (letter) {
	case 'a': name = "a_me_at_the_zoo"; break;
	case 'b': name = "b_kittens"; break;
	case 'c': name = "c_trending_today"; break;
	case 'd': name = "d_videos_worth_spreading"; break;

	}
	return name;
}



void load_input()
{
	string long_letter;
	string inputFolder;

	cout << endl << "Select input file (only first letter) -> ";
	cin >> long_letter;
	cout << "Path of the input folder -> ";
	cin >> inputFolder;
	cout << "Path of the output folder -> ";
	cin >> outputFolder;

	if (inputFolder == "0") inputFolder = IN_FOLDER;
	if (outputFolder == "0") outputFolder = OUT_FOLDER;

	fileName = getFileName(long_letter[0]);

	string inputPath = inputFolder + fileName + ".in";

	int processed = 0;
	ifstream infile(inputPath);
	if (!infile.is_open())
	{
		LOG("!!! FILE NOT FOUND !!!");
		throw uncaught_exception;
	}

	infile >> n_videos >> n_endpoints >> n_requests >> n_caches >> cache_size;

	
	for (int i = 0; i < n_videos; i++)
	{
		int size;
		infile >> size;
		video_size.push_back(size);
	}

	for (int i = 0; i < n_endpoints; i++)
	{
		endpoint e;
		int n;
		infile >> e.base_latency >> n;
		while (n--)
		{
			connection c;
			infile >> c.cache >> c.latency;
			e.conn.push_back(c);
			
		}
		endpoints.push_back(e);
	}

	for (int i = 0; i < n_requests; i++)
	{
		request r;
		infile >> r.video >> r.from >> r.count;
		r.video_size = video_size[r.video];
		requests.push_back(r);
		endpoints[r.from].requests.push_back(r);
	}
}

void writeOutputFile(vector<set<int>> &sol)
{
	ofstream outputFile;
	outputFile.open(outputPath);
	if (!outputFile.is_open())
	{
		LOG("!!! FILE NOT FOUND !!!");
		throw uncaught_exception;
	}

	outputFile << n_caches << endl;
	for (int i = 0; i < n_caches; i++)
	{
		outputFile << i << " ";
		for (int x : sol[i])
			outputFile << x << " ";
		outputFile << endl;
	}

	outputFile.close();
}

int knapsack(int* sizes, int* gains, int n, int S,string output)
{
	if (S == 0)
	{
		return 0;
	}

	if (n == 0)
	{
		return 0;
	}
	int option1 = 0;
	if (sizes[n - 1] <= S)
	{
		string var1(to_string(n - 1)); 
		string var2(" ");
		output = output + var1 + var2;
		option1 = knapsack(sizes, gains, n - 1, S - sizes[n - 1], output) + gains[n - 1];
	}

	int option2 = knapsack(sizes, gains, n - 1, S,output);

	return max(option1, option2);
	
}


int main()
{
	load_input();
	for (int i = 0; i < n_endpoints; i++)
	{
		endpoint e = endpoints[i];
		for (int j = 0; j < e.conn.size(); j++)
		{
			int* latency_gains = new int[e.requests.size()];
			int* video_sizes = new int[e.requests.size()];
			
			for (int k = 0; k < e.requests.size(); k++)
			{
				int latency_gain = (e.base_latency - e.conn[j].latency)*e.requests[k].count;
				latency_gains[k] = latency_gain;
				video_sizes[k] = e.requests[k].video_size;
			}
			string output ="";
			e.conn[j].result = knapsack(video_sizes, latency_gains, e.requests.size(), cache_size, output);
			
			
		}
	}


	return 0;
}