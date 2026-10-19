#!/bin/zsh

EXECS=("persistence")
SCALES=(3 4 5 8 11 16 22 32 45 64 90 128 181 256 362 512)
DIMENSIONS=(2 3 4 6)
FIELDS=(3 5 7 11 13)
TRIALS=${1:-10}
STRATEGIES=("twist" "JIT" "split" "stagger" "parallel" "standard")

HOST=$(hostname -f)

# Test persistence.
for EXEC in "${EXECS[@]}"; do
	for DIMENSION in "${DIMENSIONS[@]}"; do
		for FIELD in "${FIELDS[@]}"; do
			for SCALE in "${SCALES[@]}"; do
				for STRATEGY in "${STRATEGIES[@]}"; do

					PADDEDSCALE=${(l(2)(0))SCALE}
					PREFIX="$HOST.$EXEC.$STRATEGY.$PADDEDSCALE.$DIMENSION.$FIELD.cached"

					STAT="./performance/profiling/$PREFIX.stat"
					RECORD="./performance/profiling/$PREFIX.record"
					IMG="./performance/profiling/$PREFIX.png"
					FILES=($STAT $RECORD $IMG)

					for FILE in "${FILES[@]}"; do
						touch $FILE && rm $FILE
					done

					# If the files exist already, delete them.

					# perf stat -o ./performance/profiling/$PREFIX.stat ./build/profiling.$EXEC $HOST $SCALE $DIMENSION $FIELD $TRIALS $STRATEGY
					perf record --call-graph fp -o ./performance/profiling/$PREFIX.record ./build/profiling.$EXEC $HOST $SCALE $DIMENSION $FIELD $TRIALS $STRATEGY

					perf script --input=./performance/profiling/$PREFIX.record \
						| c++filt \
						| gprof2dot --format=perf --strip \
						| dot -Tpng -o ./performance/profiling/$PREFIX.png > /dev/null

					
					# ./build/timing.$EXEC $HOST $SCALE $DIMENSION $FIELD $TRIALS $STRATEGY
					# gprof ./build/profiling.$EXEC ./gmon.out > ./$DIR/profiling/$PREFIX.gprof
					# gprof ./build/profiling.$EXEC | gprof2dot --strip $ROOT | dot -Tpng -o ./$DIR/profiling/$PREFIX.png

					echo "completed $PREFIX"
					# echo $?
				done
			done
		done
	done
done