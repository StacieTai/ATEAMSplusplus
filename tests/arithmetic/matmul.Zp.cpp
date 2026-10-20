
#include <ATEAMS++/ATEAMS++.h>
#include "tests.h"

using namespace ATEAMS;
using namespace std;

int main(int argc, char* argv[]) {
	// Field; thread resources.
	Zp R(stoi(argv[1]));
	int M = stoi(argv[2]);
	int N = stoi(argv[3]);
	int TRIALS = stoi(argv[4]);
	int RESULT = PASS;

	// RNGs and stuff.
	random_device rd;
	mt19937 RNG(rd());

	uniform_int_distribution<int> uniformValues(0, R.characteristic-1);


	for (int t=0; t < TRIALS; t++) {
		// Create a random vector and a random matrix.
		SparseVector<Zp> x = randomizedVector(N, uniformValues, RNG);
		SparseMatrix<Zp> A = randomizedMatrix(M, N, uniformValues, RNG);

		SparseVector<Zp> sy = arithmetic::SparseRightMultiplication(A, x, &R);
		SparseVector<Zp> py = arithmetic::

		if (lr != rr) {
			RESULT = FAIL;
			print_vec_info<INDEX,typename Zp::dtype>(lu);
			print_vec_info<INDEX,typename Zp::dtype>(lv);
			print_vec_info<INDEX,typename Zp::dtype>(lr);

			cout << endl;

			print_vec_info<INDEX,typename Zp::dtype>(ru);
			print_vec_info<INDEX,typename Zp::dtype>(rv);
			print_vec_info<INDEX,typename Zp::dtype>(rr);

			cout << endl << endl << endl;
			break;
		}
	}

	resources.spinDown(&listener);

	return RESULT;
}
