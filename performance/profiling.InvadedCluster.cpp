
#include <ATEAMS++/ATEAMS++.h>
#include "helpers.h"

using namespace ATEAMS;
using namespace std;

using Model = models::InvadedCluster<Zp>;
using Parameters = models::ModelParameters;

using Cubical = complexes::Cubical<Model::RingType>;
using Chain = statistics::Chain<Model>;
using State = Chain::State;


int main(int argc, char* argv[]) {
	string HOSTNAME = argv[1];
	int SCALE = stoi(argv[2]);
	int DIMENSION = stoi(argv[3]);
	int FIELD = stoi(argv[4]);
	int TRIALS = stoi(argv[5]);
	int SCHEMA = stoi(argv[6]);
	
	// Construct a cubical complex.
	vector<int> corners(DIMENSION, SCALE);
	Cubical COMPLEX(corners);

	Model::RingType RR(FIELD);

	// Parametrize + initialize the model.
	Parameters PARAMETERS;
	PARAMETERS.coefficients = &RR;
	PARAMETERS.stoppingFunction = statistics::stopInvadingAt({3, 4});
	PARAMETERS.dimension = DIMENSION/2;

	Model MODEL(&COMPLEX, PARAMETERS);
	Chain CHAIN(&MODEL, TRIALS);

	for (State STATE : CHAIN.simulate()) { }
	return 0;
}