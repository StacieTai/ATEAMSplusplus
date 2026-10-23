
[![arXiv](https://img.shields.io/badge/arXiv-2507.13503-green.svg)](https://arxiv.org/abs/2507.13503)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.20817889-blue)](https://doi.org/10.5281/zenodo.20817889)
[![docs](https://img.shields.io/badge/%E2%93%98-Documentation-red)](https://apizzimenti.github.io/ATEAMSplusplus/)
[![License:MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Algebraic Topology-Enabled AlgorithMs for Spin systems, in C++

ATEAMS++ is a high-performance C++ library for simulating
[generalized Potts, random-cluster, and percolation models](https://arxiv.org/abs/2507.13503) at scale. It depends directly on [SparseRREF](https://github.com/munuxi/SparseRREF) and PHAT [[1](https://www.sciencedirect.com/science/article/pii/S0747717116300098),[2](https://bitbucket.org/phat-code/phat/src/master/)] for fast linear algebra over finite fields. It is a C++ port of the original [ATEAMS](https://github.com/apizzimenti/ATEAMS) library, now deprecated in favor of this software.


## Prerequisites

**Note:** The [Homebrew](https://brew.sh/) package manager is strongly recommended for users running macOS, any flavor of Linux, or Windows Subsystem for Linux (WSL).

The only real prerequisite is **a compiler that supports the C++23 standard.** GCC 15 is the oldest cross-compatible compiler that supports all ATEAMS++'s features. Newer versions of GCC (e.g. 16) work as well.
* **On macOS**, install [GCC 15](https://formulae.brew.sh/formula/gcc@15) [(or 16)](https://formulae.brew.sh/formula/gcc) through Homebrew. After installation, test that you have the correct version by running
	```bash
	$ g++-15 --version

	g++-15 (Homebrew GCC 15.3.0) 15.3.0
	Copyright (C) 2025 Free Software Foundation, Inc.
	This is free software; see the source for copying conditions.  There is NO
	warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	
	```
	You can set `gcc-15` and `g++-15` to be your user's default C/C++ compilers by running
	```bash
	$ echo "alias gcc=gcc-15\nalias g++=g++-15" >> ~/.zshrc
	```
	which appends aliases to your zsh configuration file (and creates the file if it doesn't already exist, which it should). You can verify that the aliases were correctly installed by running
	```bash
	$ cat ~/.zshrc

	# ... whatever else is in your .zshrc... 
	alias gcc=gcc-15
	alias g++=g++-15
	```

* **On Linux (Ubuntu 22.04/24.04)** use the same installation steps as on macOS (adjusting your shell if you're using bash), or by following [these instructions](https://askubuntu.com/a/1518433) (adjusting the version from 14 to 15).

* **On Windows,** [try MinGW](https://www.mingw-w64.org/getting-started/msys2/); it should come with a recent version of GCC.
		


## Installation

1. **Clone the repository.** In your favorite shell, navigate to a sensible directory and run
	```bash
	$ git clone --recursive https://github.com/apizzimenti/ATEAMSplusplus.git
	```
	The `--recursive` flag ensures that SparseRREF is actually cloned, not just referenced.

2. **Install dependencies.** ATEAMS++ requires

	1. [OpenMP](https://github.com/openmp),
	2. [FLINT](https://flintlib.org/), and
	3. (optionally!) [mimalloc](https://github.com/microsoft/mimalloc),

	which are all available through most package managers. [Make sure your compiler complies with the C++23 standard](https://en.cppreference.com/cpp/compiler_support/23); GCC ≥ 15 is a good bet. mimalloc is _not_ required to use this software, but it is recommended; if you don't want to use it, set the `mimalloc` variable in `CMakeLists.txt` to `FALSE` and it will be excluded.

3. **Build and install the library.** In your favorite shell, running
	```bash
	$ cd ATEAMSplusplus
	$ make build
	$ make install
	```
	will build ATEAMS++ to the `build` directory, then install its headers and bundled dependencies (SparseRREF, PHAT) to your system's default install location. If you want to install it somewhere else,
	```bash
	$ sudo cmake --install build --prefix "somewhere/else"
	```
	will do the trick.

4. **Double-check.** To verify that the library is installed correctly, running
	```bash
	$ pkg-config --cflags --libs ATEAMS++
	```
	should give something like
	```bash
	-I/usr/local/include -std=c++23 -fopenmp -Ofast -march=native -flto -funroll-loops -fprefetch-loop-arrays -fomit-frame-pointer -fno-rtti -L/usr/local/lib -lflint
	```

5. **Triple-check.** If you want to run pre-built tests, set the `TEST` variable in `CMakeLists.txt` to `TRUE`, á la
	```
	set(TEST TRUE)
	```
	then run `make test`.

## Usage

Most experiments follow a straightforward template:

1. create a Complex;
2. create a Model that consumes the Complex;
3. run a Chain on the Model.

The below example samples $`2`$-dimensional plaquette Bernoulli percolation 1,000 times on the scale-$`6`$ $`4`$-fold torus $`\mathbb T_6^4`$:

```cpp
#include <ATEAMS++.h>

using namespace ATEAMS;
using namespace std;

int main() {
	int iterations = 1000;
	int dimension = 2;

	complexes::Cubical<Z2> plex({6,6,6,6});
	models::Bernoulli percolation(&plex, dimension);
	statistics::Chain<models::Bernoulli> M(&percolation, iterations);

	vector<int> ranks(M.steps, 0);

	for (models::Bernoulli::State state : M.simulate()) { ranks[state.t] = state.rank; }

	double e = (double)accumulate(ranks.begin(), ranks.end(), 0)/(double)M.steps;
	cout << "expected rank is " << format("{:.2f}", e) << endl;

	return 0;
}
```

If the above snippet is in a file called `main.cpp`, then compiling the program and running the executable should give something like

```bash
$ $CXX main.cpp `pkg-config --libs --cflags ATEAMS++` -o main
$ ./main
expected rank is 3.09
```

This takes ~8 seconds on a 2022 MacBook Air with an Apple M2 processor. **If you plan to run large-scale simulations on an external machine, the [`magnetizationplusplus` workflow](https://github.com/apizzimenti/magnetizationplusplus) may be of use to you.**

## Known issues
* On some Linux systems, linking against ATEAMS++ after it's installed may cause some issues. In the event you get a linking error talking about undefined symbols in a `tbb` namespace, you may have to recompile your program with

	```bash
	$ $CXX yourfile.cpp `pkg-config --libs --cflags ATEAMS++` -ltbb -o executable
	```

	for things to work.

* Using `mimalloc` on macOS with GCC ≥ 16 can sometimes yield slower compute times and segfaults.
* `InvadedCluster` and `Invasion` perform $`\mathbb Z/2\mathbb Z`$ persistence when using rational coefficients.
* Some models don't have complete debugging information.


## Contributing
We welcome contributions. A few housekeeping rules:

1. **Use the fork + branch + PR flow.** Fork + clone this repository, then create a new branch for each new feature you add. Once it's camera-ready, open a pull request on the main repository page, and we'll review it.
2. **Test!** Please write unit tests (like the ones in `tests/`) for any significant features (e.g. new Models, arithmetic functions, parallelization) you add. _Pull requests without accompanying unit tests will be automatically closed._

## Citing

```bibtex
@software{ATEAMS++,
	title={{ATEAMS++: Algebraic Topology-Enabled AlgorithMs for Spin systems, in C++}},
	author={Pizzimenti, Anthony E. and Eldridge, Summer and Schweinhart, Ben and Duncan, Paul},
	url={github.com/apizzimenti/ATEAMSplusplus},
	version={1.0},
	doi={10.5281/zenodo.20817889}
}
```


