
#include <ATEAMS++/ATEAMS++.h>
#include "tests.h"

using namespace ATEAMS;
using namespace std;

using Model = models::InvadedCluster<Zp>;
using Parameters = models::ModelParameters;

using Structure = complexes::Cubical<Model::RingType>;
using State = Model::State;
using Chain = statistics::Chain<Model>;

int main(int argc, char *argv[]) {
	int FIELD = stoi(argv[1]);
	int RESULT = PASS;

	for (int dimension : DIMENSIONS) {
		vector<int> corners(dimension, 3);
		Structure COMPLEX(corners);

		Model::RingType RR(FIELD);

		Parameters PARAMETERS;
		PARAMETERS.coefficients = &RR;
		PARAMETERS.dimension = dimension/2;
		PARAMETERS.stoppingFunction = statistics::stopInvadingAt(STOPINVADING[dimension]);
		PARAMETERS.DEBUG = true;

		Model MODEL(&COMPLEX, PARAMETERS);
		Chain CHAIN(&MODEL, ITERATIONS);

		for (State STATE : CHAIN.simulate()) {
			// Figure out which cells were excluded; on these cells, the cochain
			// can evaluate to anything. We just want the ones that evaluate to
			// 0.
			vector<int> unsatisfied = statistics::unsatisfied<Model::RingType>(
				&COMPLEX, STATE.cochain, MODEL.coefficients, PARAMETERS.dimension
			);

			SparseMatrix<Model::RingType> REDUCED = MODEL.complex->Coboundary.Matrices[PARAMETERS.dimension];
			for (auto u : unsatisfied) REDUCED[u].zero();
			REDUCED.clear_zero_row();
			REDUCED.compress();

			// Verify that the sampled cochain is in the kernel of the reduced
			// coboundary matrix.
			if (!inKernel<Model::RingType>(REDUCED, STATE.cochain, MODEL.coefficients, PARAMETERS.DEBUG)) RESULT = FAIL;

			// Verify that the cochain maps to the right ring.
			if (!allEntriesIn<Model::RingType>(0, RR.characteristic, STATE.cochain)) RESULT = FAIL;
			
			// Verify that we have an appropriate number of giant cycles.
			if (STATE.rank > HOMOLOGICALRANK[dimension]) RESULT = FAIL;
		}
	}

	return RESULT;
}

