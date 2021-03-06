set(CMAKE_FIND_LIBRARY_PREFIXES "lib" "")
set(CMAKE_FIND_LIBRARY_SUFFIXES ".lib" ".a" ".so" ".sl" ".dylib" ".dll.a")

find_library(TESTC1_LIB
  NAMES testc1 testc1_test_debug_postfix
  PATHS ${top}/archive
  NO_DEFAULT_PATH)

find_library(TESTC2_LIB
  NAMES testc2 testc2_test_debug_postfix
  PATHS ${top}/archive ${top}/library
  NO_DEFAULT_PATH)

find_program(CONLY_EXE
  NAMES COnly
  PATHS ${top}/runtime
  NO_DEFAULT_PATH)

file(WRITE ${top}/OutDir.h "/* Generated by ${CMAKE_CURRENT_LIST_FILE} */
#ifndef OutDir_h
#define OutDir_h

#define TESTC1_LIB \"${TESTC1_LIB}\"
#define TESTC2_LIB \"${TESTC2_LIB}\"
#define CONLY_EXE  \"${CONLY_EXE}\"

#endif
")
