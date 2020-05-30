from conans import ConanFile, CMake, tools


class ShadercConan(ConanFile):
    name = "shaderc"
    version = "b4a735cc"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "lto": [True, False]}
    default_options = {"shared": False, "lto": False}
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/google/shaderc.git")
        self.run("cd shaderc && git checkout b4a735cc")
        tools.replace_in_file("shaderc/CMakeLists.txt", 
            "project(shaderc)", 
            '''project(shaderc)
            include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
            conan_basic_setup()'''
        )
        tools.replace_in_file("shaderc/CMakeLists.txt", 
            "add_subdirectory(third_party)", ""
        )
        tools.replace_in_file("shaderc/CMakeLists.txt", 
            "add_subdirectory(examples)", ""
        )
        tools.replace_in_file("shaderc/CMakeLists.txt", 
            "add_subdirectory(glslc)", ""
        )
        tools.replace_in_file("shaderc/CMakeLists.txt", 
            '''add_custom_target(build-version
  ${PYTHON_EXECUTABLE}
  ${CMAKE_CURRENT_SOURCE_DIR}/utils/update_build_version.py
  ${shaderc_SOURCE_DIR} ${spirv-tools_SOURCE_DIR} ${glslang_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/build-version.inc
  COMMENT "Update build-version.inc in the Shaderc build directory (if necessary).")''', 
            ""
        )
        tools.replace_in_file("shaderc/libshaderc_util/CMakeLists.txt", 
            "glslang OSDependent OGLCompiler HLSL glslang SPIRV", 
            "${CONAN_LIBS}"
        )
        tools.replace_in_file("shaderc/libshaderc_util/CMakeLists.txt", 
            "SPIRV-Tools-opt ${CMAKE_THREAD_LIBS_INIT})", 
            "${CMAKE_THREAD_LIBS_INIT})"
        )
        tools.replace_in_file("shaderc/libshaderc/CMakeLists.txt", 
            '''set(SHADERC_LIBS
  glslang OSDependent OGLCompiler glslang ${CMAKE_THREAD_LIBS_INIT}
  shaderc_util
  SPIRV # from glslang
  SPIRV-Tools
)''', 
            '''set(SHADERC_LIBS
  ${CMAKE_THREAD_LIBS_INIT}
  shaderc_util ${CONAN_LIBS}
)'''
        )
        tools.replace_in_file("shaderc/glslc/CMakeLists.txt", 
            '''target_link_libraries(glslc PRIVATE glslang OSDependent OGLCompiler
  HLSL glslang SPIRV ${CMAKE_THREAD_LIBS_INIT})''', 
            '''target_link_libraries(glslc PRIVATE ${CONAN_LIBS} ${CMAKE_THREAD_LIBS_INIT})'''
        )
        tools.replace_in_file("shaderc/glslc/src/main.cc", 
            '''#include "build-version.inc"''', '''"version"'''
        )

    def requirements(self):
        self.requires.add("SPIRV-Tools/e128ab0d", private=False)
        self.requires.add("glslang/d39b8afc", private=False)

    def build(self):
        cmake = CMake(self)

        cmake_linker_flags = ""
        if self.options.lto == True:
            cmake_linker_flags += " -fuse-ld=gold -fuse-linker-plugin "
            cmake.definitions["CMAKE_INTERPROCEDURAL_OPTIMIZATION"] = "TRUE"

        if not cmake_linker_flags:
            cmake.definitions["CMAKE_EXE_LINKER_FLAGS"] = cmake_linker_flags

        cmake.definitions["SHADERC_SKIP_TESTS"] = 'ON'
        cmake.definitions["SHADERC_ENABLE_SPVC"] = 'OFF'
        
        cmake.configure(source_folder="shaderc")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["shaderc_combined"]
        if self.options.shared:
            self.cpp_info.libs.append("shaderc_shared")
        else:
            self.cpp_info.libs.append("shaderc")
        
        self.cpp_info.libdirs = ['lib', 'lib64']
