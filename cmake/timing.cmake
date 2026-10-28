
################################################################################
## Timing configurations.                                                     ##
################################################################################


list(APPEND ARITHMETIC.TIMING
	"addition"
)

list(APPEND MODELS.TIMING
	"Bernoulli"
	"InvadedCluster"
	"Invasion"
	"SwendsenWang"
	"Glauber"
)

list(APPEND TOPOLOGY.TIMING
	"persistence"
)

if (TIMING)
	if(TIMING_MODELS)
		foreach(MODEL IN LISTS MODELS.TIMING)
			add_executable(timing.${MODEL} performance/timing.${MODEL}.cpp)
			target_link_libraries(timing.${MODEL} PUBLIC ATEAMS++)
			target_compile_options(timing.${MODEL} PUBLIC ${TIMING_COMPILE_OPTIONS})
		endforeach()
	endif()

	if(TIMING_TOPOLOGY)
		foreach(FUNCTION IN LISTS TOPOLOGY.TIMING)
			add_executable(timing.${FUNCTION} performance/timing.${FUNCTION}.cpp)
			target_link_libraries(timing.${FUNCTION} PUBLIC ATEAMS++)
			target_compile_options(timing.${FUNCTION} PUBLIC ${TIMING_COMPILE_OPTIONS})
		endforeach()
	endif()

	if(TIMING_ARITHMETIC)
		foreach(FUNCTION IN LISTS ARITHMETIC.TIMING)
			add_executable(timing.${FUNCTION} performance/timing.${FUNCTION}.cpp)
			target_link_libraries(timing.${FUNCTION} PUBLIC ATEAMS++)
			target_compile_options(timing.${FUNCTION} PUBLIC ${TIMING_COMPILE_OPTIONS})
		endforeach()
	endif()
endif()
