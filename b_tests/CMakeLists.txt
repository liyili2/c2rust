cmake_minimum_required(VERSION 3.13.4)
project(PointerSafetyExamples VERSION 1.0)

# Set the C standard
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED True)

# Optionally, enable the export of compile commands if needed for tools like c2rust
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# List all source files here
set(SOURCE_FILES
    b10_allsafepointerstruct.c
    b11_calleestructnp.c
    b12_callerstructnp.c
    b13_calleestructp.c
    b14_callerstructp.c
    b15_calleepointerstruct.c
    b16_callerpointerstruct.c
    b17_bothstructnp.c
    b18_bothstructp.c
    b19_bothpointerstruct.c
    b1_allsafe.c
    b20_allsafepointerstructproto.c
    b21_calleepointerstructproto.c
    b22_callerpointerstructproto.c
    b23_explicitunsafecast.c
    b23_retswitchexplicit.c
    b24_implicitunsafecast.c
    b24_retswitchimplicit.c
    b25_castprotosafe.c
    b26_castprotounsafe.c
    b26_castprotounsafeimplicit.c
    b26_castprotounsafeimplicitretswitch.c
    b27_structcastsafe.c
    b28_structcastexplicit.c
    b28_structcastimplicit.c
    b28_structimplicitretcast.c
    b29_structprotocastsafe.c
    b29_structprotocastsafeuseunsafe.c
    b2_calleeunsafe.c
    b30_structprotocastexplicitunsafeuseunsafe.c
    b30_structprotocastimplicitunsafeuseunsafe.c
    b30_structprotocastunsafeexplicit.c
    b30_structprotocastunsafeimplicit.c
    b30_structprotocastunsafeimplicitretswitch.c
    b30_structprotoconflictbodyconvert.c
    b30_structprotoconflict.c
    b3_onecallerunsafe.c
    b4_bothunsafe.c
    b5_calleeunsafeproto.c
    b6_callerunsafeproto.c
    b7_allsafeproto.c
    b8_allsafestructnp.c
    b9_allsafestructp.c
    # Exclude output.txt from compilation
)

# Create an executable with all source files
add_executable(PointerSafety ${SOURCE_FILES})

# If you have additional libraries to link or include directories to add, do so here
# target_link_libraries(PointerSafety some_library)
# include_directories(some_include_directory)

