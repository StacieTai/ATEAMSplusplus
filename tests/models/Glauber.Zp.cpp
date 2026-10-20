
#include <ATEAMS++/ATEAMS++.h>
#include "tests.h"

using namespace ATEAMS;
using namespace std;

using Model = models::Glauber<Zp>;
using Parameters = models::ModelParameters;

using Structure = complexes::Cubical<Model::RingType>;
using State = Model::State;
using Chain = statistics::Chain<Model>;

int main(int argc, char *argv[]) {
	int FIELD = stoi(argv[1]);
	int RESULT = PASS;

	for (int dimension : DIMENSIONS) {
		vector<int> corners(dimension, 3);
		Structure CUBICAL(corners);

		Model::RingType RR(FIELD);

		Parameters PARAMETERS;
		PARAMETERS.coefficients = &RR;
		PARAMETERS.dimension = dimension/2;
		PARAMETERS.temperatureFunction = statistics::selfdual(PARAMETERS.coefficients);
		PARAMETERS.DEBUG = true;

		Model MODEL(&CUBICAL, PARAMETERS);
		Chain CHAIN(&MODEL, ITERATIONS);

		for (State STATE : CHAIN.simulate()) {
			// Check that the cochain maps to the right ring.
			if (!allEntriesIn<Model::RingType>(0, RR.characteristic, STATE.cochain)) RESULT = FAIL;
		}
	}

	return RESULT;
}

