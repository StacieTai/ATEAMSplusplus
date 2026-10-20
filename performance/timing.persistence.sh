#!/bin/zsh

EXECS=("persistence")
SCALES=(3 4 5 8 11 16 22 32 45 64 90 128 181 256 362 512)
DIMENSIONS=(2 3 4 6)
FIELDS=(3)
TRIALS=${1:-100}
STRATEGIES=("twist" "JIT" "split" "stagger")

HOST=$(hostname -f)
printf -v BREAK "—%.0s" {1..42}
TIMEFMT=$'%E'

# Test persistence.
for EXEC in "${EXECS[@]}"; do
	printf "%-7s %-7s %-7s %-7s %10s%s\n" "DIM" "SCALE" "FIELD" "TRIALS" "VARIANT"
	echo $BREAK
	for DIMENSION in "${DIMENSIONS[@]}"; do
		for FIELD in "${FIELDS[@]}"; do
			for SCALE in "${SCALES[@]}"; do
				# # Execute all the strategies at once.
				# exec=""
				# for STRATEGY in "${STRATEGIES[@]}"; do
				# 	# Delete the file if it exists already.
				# 	# CSV="./performance/timing/$HOST.persistence.$STRATEGY.$TRIALS.csv"
				# 	# touch $CSV && rm $CSV

				# 	# Run the script.
				# 	exec+="./build/timing.$EXEC $HOST $SCALE $DIMENSION $FIELD $TRIALS $STRATEGY &"
				# 	# ./build/timing.$EXEC $HOST $SCALE $DIMENSION $FIELD $TRIALS $STRATEGY
				# 	# echo $?
				# done

				# PADDEDSCALE="SCALE ${(r(3)( ))SCALE}"
				# PADDEDFIELD="FIELD ${(r(3)( ))FIELD}"

				# echo "starting\t$HOST $PADDEDSCALE DIMENSION $DIMENSION $PADDEDFIELD TRIALS $TRIALS"
				# eval $exec
				# wait

				# echo "completed\t$HOST $PADDEDSCALE DIMENSION $DIMENSION $PADDEDFIELD TRIALS $TRIALS \n"

				for STRATEGY in "${STRATEGIES[@]}"; do
					PADDEDSCALE="SCALE ${(r(3)( ))SCALE}"
					PADDEDFIELD="FIELD ${(r(3)( ))FIELD}"

					# Run the script.
					printf "%-7s %-7s %-7s %-7s %10s..." $DIMENSION $SCALE $FIELD $TRIALS $STRATEGY
					# ./build/timing.$EXEC $HOST $SCALE $DIMENSION $FIELD $TRIALS $STRATEGY
					ttc=$( { time ./build/timing.$EXEC $HOST $SCALE $DIMENSION $FIELD $TRIALS $STRATEGY; } 2>&1 )
					# echo "completed\t$HOST $PADDEDSCALE DIMENSION $DIMENSION $PADDEDFIELD TRIALS $TRIALS\n"
					printf " done in $ttc\n"
					# printf " done.\n"
				done
				echo $BREAK
			done
			echo $BREAK
		done
		echo $BREAK
	done
done