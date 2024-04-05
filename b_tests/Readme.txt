
Generating compile_commands.json


with cmake :
When creating the initial build directory with cmake specify -DCMAKE_EXPORT_COMPILE_COMMANDS=1. This only works on projects configured to be built by cmake. This works on Linux and MacOS.



cmake ../dir -DCMAKE_EXPORT_COMPILE_COMMANDS=1
cmake --build
c2rust transpile compile_commands.json
