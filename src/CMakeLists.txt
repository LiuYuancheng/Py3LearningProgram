# libs are stored in KeyExchangeApp\app\src\main\jniLibs
# For more information about using CMake with Android Studio, read the
# documentation: https://d.android.com/studio/projects/add-native-code.html

# Sets the minimum version of CMake required to build the native library.

cmake_minimum_required(VERSION 3.4.1)
#set(CMAKE_C_COMPILER clang++)
#set(CMAKE_CXX_COMPILER clang++)

include_directories(${CMAKE_SOURCE_DIR}/include)
# Creates and names a library, sets it as either STATIC
# or SHARED, and provides the relative paths to its source code.
# You can define multiple libraries, and CMake builds them for you.
# Gradle automatically packages shared libraries with your APK.
file(GLOB_RECURSE KemsSOURCE "generic_service/kems/*.h" "generic_service/kems/*.cpp" )
file(GLOB_RECURSE KepsSOURCE "generic_service/keps/*.h" "generic_service/keps/*.cpp")
file(GLOB_RECURSE LKepsSOURCE "generic_service/lower_keps/*.h" "generic_service/lower_keps/*.cpp")
file(GLOB_RECURSE commSOURCE "generic_service/comm/*.h" "generic_service/comm/*.cpp")
file(GLOB pqcSOURCE "NIST_PQC_Round1/*.h" "NIST_PQC_Round1/*.cpp")
#file(GLOB mbedSOURCE "include/mbeds/*.h")
file(GLOB_RECURSE mainSOURCE "generic_service/*.h" "generic_service/*.cpp")
file(GLOB_RECURSE libconfigSOURCE "include/*.c" "include/*.cpp")

add_library( # Sets the name of the library.
        native-lib

        # Sets the library as a shared library.
        SHARED

        # Provides a relative path to your source file(s).
        ${KemsSOURCE}
        ${KepsSOURCE}
        ${LKepsSOURCE}
        ${commSOURCE}
        #${mbedSOURCE}
        ${mainSOURCE}

        ${CMAKE_SOURCE_DIR}/include/libconfig.c
        ${CMAKE_SOURCE_DIR}/include/scanctx.c
        native-lib.cpp
        )

target_include_directories( native-lib PRIVATE
        ${CMAKE_SOURCE_DIR}/generic_service
        ${CMAKE_SOURCE_DIR}/generic_service/keps
        ${CMAKE_SOURCE_DIR}/generic_service/kems
        ${CMAKE_SOURCE_DIR}/generic_service/lower_keps
)



# Searches for a specified prebuilt library and stores the path as a
# variable. Because CMake includes system libraries in the search path by
# default, you only need to specify the name of the public NDK library
# you want to add. CMake verifies that the library exists before
# completing its build.

find_library( # Sets the name of the path variable.
        log-lib

        # Specifies the name of the NDK library that
        # you want CMake to locate.
        log )

# Specifies libraries CMake should link to your target library. You
# can link multiple libraries, such as libraries you define in this
# build script, prebuilt third-party libraries, or system libraries.

target_link_libraries( # Specifies the target library.
        native-lib

        # Links the target library to the log library
        # included in the NDK.
        ${log-lib} )

include_directories(${CMAKE_SOURCE_DIR}/include)
include_directories(${CMAKE_SOURCE_DIR}/lib)

target_link_libraries(native-lib
        ${CMAKE_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libgf2x.so
        ${CMAKE_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libgmp.so
        ${CMAKE_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libmbedcrypto.a
        ${CMAKE_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libmbedtls.a

        ${CMAKE_SOURCE_DIR}/../jniLibs/${ANDROID_ABI}/libcrypto.so
        )