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
typedef long long ll;

string inputFolder;
string outputFolder;
string inputPath;
string outputPath;
ofstream outputFile;
ifstream inputFile;

string getFileName(char letter)
{
	string name;
	switch (letter) {
	case 'a': name = "a_example"; break;
	case 'b': name = "b_read_on"; break;
	case 'c': name = "c_incunabula"; break;
	case 'd': name = "d_tough_choices"; break;
	case 'e': name = "e_so_many_books"; break;
	case 'f': name = "f_libraries_of_the_world"; break;
	default:break;
	}
	return name;
}
char letter;
void readInputFile()
{
	cout << endl << "Select input file (only first letter) -> ";
	cin >> letter;
	cout << "Path of the input folder -> ";
	cin >> inputFolder;
	cout << "Path of the output folder -> ";
	cin >> outputFolder;

	if (inputFolder == "0") inputFolder = IN_FOLDER;
	if (outputFolder == "0") outputFolder = OUT_FOLDER;

	string fileName = getFileName(letter);

	inputPath = inputFolder + fileName + ".txt";

	int processed = 0;
	inputFile.open(inputPath);
	if (!inputFile.is_open())
	{
		LOG("!!! FILE NOT FOUND !!!");
		throw uncaught_exception;
	}

}
vector<pair<int, vector<int>>> ans;
int L;
void writeOutputFile()
{
	outputPath = outputFolder + getFileName(letter) + ".out";
	outputFile.open(outputPath);
	if (!outputFile.is_open())
	{
		LOG("!!! FILE NOT FOUND !!!");
		throw uncaught_exception;
	}

	outputFile << ans.size() << '\n';
	for (auto p : ans) {
		outputFile << p.first << ' ' << p.second.size() << '\n';
		for (auto e : p.second)outputFile << e << ' ';
		outputFile << '\n';
	}

	outputFile.close();
}

struct book {
	int id, score;
	bool used;
	int g;
};
struct library {
	int id, t, m, n;
	vector<int> b;
	bool sign;
};
int B, D, N, i, j, signup;
vector<library> l;
vector<book> books;

ll score;

int chooseLibrary() {
	int r = -1, k;
	ll points = 0, temp, bleft, s, d;
	for (int j = 0; j < L; ++j) {
		if (l[j].sign)continue;
		k = temp = 0;
		bleft = (D - i - l[j].t) / l[j].m;
		//How much value can you bring until last day
		for (int b : l[j].b) {
			if (k >= bleft)break;
			if (books[b].used || l[j].m > 1.666*books[b].g)continue;

			++k;
			temp += books[b].score;
		}

		if (temp > points) {
			points = temp;
			r = j;
		}
	}

	if (r == -1)return -1;

	k = 0;
	pair<int, vector<int>> w;
	w.first = r;
	for (int j = 0; j < l[r].b.size() && k < bleft; ++j) {
		if (!books[l[r].b[j]].used) {
			w.second.push_back(l[r].b[j]);
			books[l[r].b[j]].used = true;
			++k;
		}
	}
	if (w.second.size() > 0) {
		ans.push_back(w);
	}
	l[r].sign = true;

	score += points;
	return r;
}

bool comp(int x, int y) {
	return books[x].score > books[y].score;
}

int main()
{
	readInputFile();
	inputFile >> B >> L >> D;
	books.resize(B);
	for (i = 0; i < B; ++i) {
		inputFile >> books[i].score;
		books[i].id = i;
		books[i].used = false;
		books[i].g = 0;
	}
	l.resize(L);
	for (i = 0; i < L; ++i) {
		int n;
		l[i].sign = false;
		inputFile >> n >> l[i].t >> l[i].m;
		l[i].b.resize(n);
		for (j = 0; j < n; ++j) {
			int b;
			inputFile >> b;
			if (books[b].g == 0)books[b].g = l[i].m;
			else books[b].g = min(books[b].g, l[i].m);
			l[i].b[j] = b;
		}
		sort(l[i].b.begin(), l[i].b.end(), comp);
	}

	for (i = 0; i < D;) {
		int r;
		r = chooseLibrary();
		if (r == -1)break;
		i += l[r].t;

		cout << i << '\n';
	}

	writeOutputFile();
	cerr << score;
}


/*
good:
	m is low
	valuable unused books
	t is low

bad:

*/


/*
for (j = 0; j < sl.size(); ++j) {
			if(sl[j].ended)continue;
			int lib = sl[j].id;
			int book = sl[j].index;
			while (1) {

				if (book < l[lib].b.size() && books[l[lib].b[book]].tobeused != sl[j].id)book++;
				if (book == l[lib].b.size()) {
					sl[j].ended = true;
					break;
				}
				else {
					int pom = l[lib].b[book];
					ans[lib].push_back(books[pom].id);
					books[pom].used = true;
				}
				//if(index+1==l[x.id])
			}

		}
*/