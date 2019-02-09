from conans import ConanFile, CMake, tools


class GoogletestConan(ConanFile):
    name = "googletest"
    version = "1.8"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Googletest here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "lto": [True, False]}
    default_options = {"shared": False, "lto": False}
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/google/googletest")
        self.run("cd googletest && git checkout release-1.8.0")
        tools.replace_in_file("googletest/CMakeLists.txt", "project( googletest-distribution )", '''project( googletest-distribution ) 
            include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake) 
            conan_basic_setup()'''
        )

    def build(self):
        cmake = CMake(self)

        cmake_linker_flags = ""
        if self.options.lto == True:
            cmake_linker_flags += " -fuse-ld=gold -fuse-linker-plugin "
            cmake.definitions["CMAKE_INTERPROCEDURAL_OPTIMIZATION"] = "TRUE"

        if not cmake_linker_flags:
            cmake.definitions["CMAKE_EXE_LINKER_FLAGS"] = cmake_linker_flags

        cmake.configure(source_folder=f"{self.source_folder}/googletest")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["gmock", "gmock_main", "gtest", "gtest_main"]
        self.cpp_info.libdirs = ['lib', 'lib64']