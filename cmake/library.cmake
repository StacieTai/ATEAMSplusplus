
################################################################################
## Source headers and header implementation files.                            ##
################################################################################

# Headers (include/ATEAMS++/*.h)
list(APPEND SOURCE_HEADERS
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/common.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/util.h

	${PROJECT_SOURCE_DIR}/include/ATEAMS++/arithmetic/arithmetic.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/arithmetic/kernel.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/arithmetic/resources.h

	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/topology.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/persistence.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/helpers.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/persistence/JIT.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/persistence/parallel.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/persistence/PHAT.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/persistence/split.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/persistence/stagger.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/persistence/standard.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/persistence/twist.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/persistence/reduction.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/topology/persistence/policies.h

	${PROJECT_SOURCE_DIR}/include/ATEAMS++/complexes/complexes.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/complexes/Complex.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/complexes/Cubical.h

	${PROJECT_SOURCE_DIR}/include/ATEAMS++/models/models.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/models/ModelState.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/models/ModelParameters.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/models/Model.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/models/Bernoulli.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/models/Glauber.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/models/InvadedCluster.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/models/SwendsenWang.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/models/Invasion.h

	${PROJECT_SOURCE_DIR}/include/ATEAMS++/statistics/statistics.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/statistics/Chain.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/statistics/observables.h
	${PROJECT_SOURCE_DIR}/include/ATEAMS++/statistics/schedules.h
)


# Templated implementations (src/ATEAMS++/*.tpp)
list(APPEND SOURCE_IMPLEMENTATIONS
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/arithmetic/kernel.tpp
	
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/topology/persistence/JIT.tpp
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/topology/persistence/parallel.tpp
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/topology/persistence/PHAT.tpp
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/topology/persistence/split.tpp
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/topology/persistence/stagger.tpp
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/topology/persistence/standard.tpp
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/topology/persistence/twist.tpp

	${PROJECT_SOURCE_DIR}/src/ATEAMS++/complexes/Cubical.tpp

	${PROJECT_SOURCE_DIR}/src/ATEAMS++/models/SwendsenWang.tpp
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/models/Bernoulli.tpp
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/models/Glauber.tpp
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/models/InvadedCluster.tpp
	${PROJECT_SOURCE_DIR}/src/ATEAMS++/models/Invasion.tpp
)