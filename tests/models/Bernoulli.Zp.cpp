
#include <ATEAMS++/ATEAMS++.h>
#include "tests.h"

using namespace ATEAMS;
using namespace std;

using Model = models::Bernoulli;
using Parameters = models::ModelParameters;

using Structure = complexes::Cubical<Model::RingType>;
using State = models::Bernoulli::State;
using Chain = statistics::Chain<models::Bernoulli>;

int main(int argc, char *argv[]) {
	int FIELD = stoi(argv[1]);
	int RESULT = PASS;

	for (int dimension : DIMENSIONS) {
		vector<int> corners(dimension, 3);
		Structure COMPLEX(corners);

		Parameters PARAMETERS;
		PARAMETERS.p = 0.5;
		PARAMETERS.dimension = dimension/2;
		PARAMETERS.DEBUG = true;

		Model MODEL(&COMPLEX, PARAMETERS);
		Chain CHAIN(&MODEL, ITERATIONS);

		vector<int> RANKS;
		int low = 0, high = COMPLEX.Cells[PARAMETERS.dimension];

		for (State STATE : CHAIN.simulate()) {
			// Check that we have an appropriate number of giant cycles.
			if (STATE.rank > HOMOLOGICALRANK[dimension]) RESULT = FAIL;
			RANKS.push_back(STATE.rank);

			// Check that all the included values are between 0 and the number
			// of d-cells.
			for (auto& t : STATE.includes) {
				if (!(low <= t && t <= high)) RESULT = FAIL;
			}
		}

		// In the even dimensions, check whether all the ranks were the same;
		// if so, there's something weird going on.
		if (!dimension%2 && std::equal(RANKS.begin()+1, RANKS.end(), RANKS.begin())) RESULT = FAIL;
	}

	return RESULT;
}

