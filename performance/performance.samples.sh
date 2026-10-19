#!/bin/zsh

SCALES=(3 4 5 8 11 16 22 32 45 64 90 128 181 256 362 512)
DIMENSIONS=(2 3 4 6)
TRIALS=${1:-100}


for DIMENSION in "${DIMENSIONS[@]}"; do
	for SCALE in "${SCALES[@]}"; do
		for FIELD in "${FIELDS[@]}"; do
			PADDEDSCALE=${(l(3)( ))SCALE}
			./build/performance.samples $SCALE $DIMENSION $TRIALS
			echo "completed $PADDEDSCALE $DIMENSION $TRIALS"
		done
	done
done