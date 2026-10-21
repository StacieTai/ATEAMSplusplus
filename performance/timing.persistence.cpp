
#include <ATEAMS++/ATEAMS++.h>
#include <time.h>
#include "helpers.h"

using namespace ATEAMS;
using namespace ATEAMS::topology;
using namespace std;

// From https://www.guyrutenberg.com/2007/09/22/profiling-code-using-clock_gettime/
timespec diff(timespec& end, timespec& start) {
	timespec temp;

	if (end.tv_nsec-start.tv_nsec < 0) {
		temp.tv_sec = end.tv_sec-start.tv_sec-1;
		temp.tv_nsec = 1e9 + end.tv_nsec-start.tv_nsec;
	} else {
		temp.tv_sec = end.tv_sec-start.tv_sec;
		temp.tv_nsec = end.tv_nsec-start.tv_nsec;
	}

	return temp;
}


double tstime(timespec& end, timespec& start) {
	timespec delta = diff(end, start);
	return delta.tv_sec + delta.tv_nsec;
}


void monocputime(timespec& ts) {
	clock_gettime(CLOCK_MONOTONIC, &ts);
}

void threadcputime(timespec& ts) {
	clock_gettime(CLOCK_THREAD_CPUTIME_ID, &ts);
}

auto steadycputime(
	vector<int>& filtration,
	auto& reduction
) {
	auto start = chrono::steady_clock::now();
	reduction(filtration);
	auto end = chrono::steady_clock::now();

	return chrono::duration_cast<chrono::microseconds>(end-start).count();
}


std::function<void(vector<int>&)> reducer(
	string& STRATEGY,
	complexes::Cubical<Zp>& plex,
	Zp& R,
	arithmetic::ComputeResources<Zp>& resources
) {
	// Uncomment to verify that there's no overhead (i.e. variable copying)
	// that spoils the comparison.
	// return [&](vector<int>& K) { };

	if (STRATEGY == "JIT") {
		return [&](vector<int>& K) {
			persistence::JIT<Zp>(&plex, K, &R, resources);
		};
	} else if (STRATEGY == "twist") {
		return [&](vector<int>& K) {
			persistence::twist<Zp>(&plex, K, &R, resources);
		};
	} else if (STRATEGY == "standard") {
		return [&](vector<int>& K) {
			persistence::standard<Zp>(&plex, K, &R, resources);
		};
	} else if (STRATEGY == "stagger") {
		return [&](vector<int>& K) {
			persistence::stagger<Zp>(&plex, K, &R, resources);
		};
	} else if (STRATEGY == "split") {
		return [&](vector<int>& K) {
			persistence::split<Zp>(&plex, K, &R, resources);
		};
	} else {
		return [&](vector<int>& K) {
			persistence::parallel<Zp>(&plex, K, &R, resources);
		};
	}
}


int main(int argc, char* argv[]) {
	string HOSTNAME = argv[1];
	int SCALE = stoi(argv[2]);
	int DIMENSION = stoi(argv[3]);
	int FIELD = stoi(argv[4]);
	int TRIALS = stoi(argv[5]);
	string STRATEGY = argv[6];

	if (shouldQuit(SCALE, DIMENSION)) return 0;

	// Construct a cubical complex and the ingredients for a filtration.
	Zp R(FIELD);
	complexes::Cubical<Zp> plex(vector<int>(DIMENSION, SCALE));
	plex.constructBoundaryMatrices(&R);
	plex.constructFullBoundaryMatrix(&R);

	// Read in the sample filtrations.
	vector<vector<int>> filtrations = filtrationData(plex.size(), SCALE, DIMENSION, TRIALS);
	
	// Create compute resources.
	arithmetic::ComputeResources<Zp> resources;

	thread listener = resources.spinUp();
	resources.arithmetize(&R);
	resources.parallel->enabled = true;
	resources.parallel->build(plex.size(), plex.Cells.size());
	resources.serial->build(plex.size());

	auto method = reducer(STRATEGY, plex, R, resources);


	// Create a bucket for storing times to completion.
	vector<int> TTC(TRIALS);

	for (int t=0; t < TRIALS; t++) {
		// Create the filtration.
		vector<int> K = filtrations[t];

		// Time, then write the data to storage.
		TTC[t] = steadycputime(K, method);
	}

	// Write data to file.
	string csv = "";

	for (int t=0; t < TRIALS; t++) {
		csv = csv + format(
			"{},{},{},{}\n",
			SCALE,
			DIMENSION,
			FIELD,
			TTC[t]
		);
	}

	// Spin down the listener.
	resources.spinDown(&listener);

	// APPEND to file.
	ofstream file;
	file.open(format("./performance/timing/{}.persistence.{}.{}.csv", HOSTNAME, STRATEGY, TRIALS), fstream::app);
	file << csv;
	file.close();

	return 0;
}