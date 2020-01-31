#pragma once
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

using namespace std;
typedef long long ll;
#define LOG(x) cout << (x) << endl

int h, w, cnt_cars, cnt_rides, bonus_start,T;
string inputPath;
vector<int> in;
int total_score = 0;
vector<vector<int>> output;
int super;
string outputPath;

int dist(const pair<int, int> & a, const pair<int, int> & b) {
	return abs(a.first - b.first) + abs(a.second - b.second);
}

struct Ride {
	pair<int, int> start, end;
	int when_start, when_end;
	int id;
	void read(int _id) {
		id = _id;
		start.first = in.front();
		in.erase(in.begin());
		start.second = in.front();
		in.erase(in.begin());
		end.first = in.front();
		in.erase(in.begin());
		end.second = in.front();
		in.erase(in.begin());
		when_start = in.front();
		in.erase(in.begin());
		when_end = in.front();
		in.erase(in.begin());
	}
	int length() const {
		return dist(start, end);
	}
};



struct Car {
	pair<int, int> where;
	int when;
	int id;
	int when_can_get(const pair<int, int> & a) const {
		return when + dist(where, a);
	}
	int real_simulate(const Ride & ride, bool indeed) {
		ll score = 0;
		when += dist(where, ride.start);
		if (when <= ride.when_start) {
			if (indeed) ++super;
			when = ride.when_start;
			score += bonus_start;
		}
		when += ride.length();
		if (when <= ride.when_end) {
			score += ride.length();
		}
		else {
			assert(!indeed);
			score = 0;
		}
		where = ride.end;
		return score;
	}
	int fake_simulate(const Ride & ride) const {
		Car x = *this;
		return x.real_simulate(ride, false);
	}
	int would_wait(const Ride & ride) const {
		int get_there = when_can_get(ride.start);
		return max(0, ride.when_start - get_there);
	}
	int would_need(const Ride & ride) const {
		return max(when_can_get(ride.start), ride.when_start) - when;
	}
	void add_ride(const Ride & ride) const {
		output[id].push_back(ride.id);
	}
};



string getFileName(char letter)
{
	string name;
	switch (letter) {
	case 'a': name = "a_example"; break;
	case 'b': name = "b_should_be_easy"; break;
	case 'c': name = "c_no_hurry"; break;
	case 'd': name = "d_metropolis"; break;
	case 'e': name = "e_high_bonus"; break;
	}
	return name;
}


void writeOutputFile()
{
	ofstream outputFile;
	outputFile.open(outputPath);
	if (!outputFile.is_open())
	{
		LOG("!!! FILE NOT FOUND !!!");
		throw uncaught_exception;
	}
	for (int i = 0; i < cnt_cars; ++i) {
		outputFile << (int)output[i].size() <<" ";
		for (int x : output[i])
			outputFile << x << " ";
		outputFile << endl;
	}
	outputFile.close();
}

void createOutputFile()
{
	ofstream outfile(outputPath);

	outfile << "my text here!" << endl;

	outfile.close();


}

int solve() {

	output.resize(cnt_cars);

	vector<Ride> rides(cnt_rides);
	for (int i = 0; i < cnt_rides; ++i)
		rides[i].read(i);


	vector<Car> cars(cnt_cars);
	for (int i = 0; i < cnt_cars; ++i)
		cars[i].id = i;

	vector<bool> done(cnt_rides);

	
	int AC = 0;

	vector<int> far(cnt_rides, INT_MAX);
	for (int i = 0; i < cnt_rides; ++i) if (!done[i])
		for (int j = 0; j < cnt_rides; ++j) if (i != j) if (!done[j])
			far[i] = min(far[i], dist(rides[i].end, rides[j].start));

	while (true) {
		bool anything = false;

		for (Car & car : cars) {
			pair<int, int> best;
			best.first = INT_MAX;
			for (int i = 0; i < cnt_rides; ++i) if (!done[i]) {
				int would_score = car.fake_simulate(rides[i]);
				if (would_score == 0) continue; // can't do it in time
					int wasted = car.would_need(rides[i]);
				int when_would_finish = car.when + wasted + rides[i].length();
				if (when_would_finish <= T * 0.98) wasted += far[i] / 15;
				best = min(best, { wasted, i });
			}
			if (best.first == INT_MAX) continue;
			int i = best.second;
			done[i] = true;
			int tmp = car.real_simulate(rides[i], true);
			total_score += tmp;
			anything = true;
			car.add_ride(rides[i]);
			++AC;
		}
		if (!anything) break;
	}
	
	cerr << "score = " << total_score << "\n";
	
	
	return 0;
}




int main()
{

	string long_letter;
	string inputFolder;
	string outputFolder;

	cout << endl << "Select input file (only first letter) -> ";
	cin >> long_letter;
	cout << "Path of the input folder -> ";
	cin >> inputFolder;
	cout << "Path of the output folder -> ";
	cin >> outputFolder;

	if (inputFolder == "0") inputFolder = IN_FOLDER;
	if (outputFolder == "0") outputFolder = OUT_FOLDER;

	string fileName = getFileName(long_letter[0]);

	inputPath = inputFolder + fileName + ".in";

	int processed = 0;
	ifstream infile(inputPath);
	if (!infile.is_open())
	{
		LOG("!!! FILE NOT FOUND !!!");
		throw uncaught_exception;
	}
	

	int row, col, v, n, bonus, t;
	int a, b, x, y, s, f;
	
	infile >> h >> w >> cnt_cars >> cnt_rides >> bonus_start >> T;
	
	while (infile >> a >> b >> x >> y >> s >> f)
	{
		in.push_back(a);
		in.push_back(b);
		in.push_back(x);
		in.push_back(y);
		in.push_back(s);
		in.push_back(f);

	}

	
	solve();
	outputPath = outputFolder + fileName + "_" + to_string(total_score) + "_Simran_.out";
	writeOutputFile();
	cin.get();
}











