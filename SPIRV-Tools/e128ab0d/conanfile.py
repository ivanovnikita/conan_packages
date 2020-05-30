from conans import ConanFile, CMake, tools


class SpirvtoolsConan(ConanFile):
    name = "SPIRV-Tools"
    version = "e128ab0d"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "lto": [True, False]}
    default_options = {"shared": False, "lto": False}
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/KhronosGroup/SPIRV-Tools.git")
        self.run("cd SPIRV-Tools && git checkout e128ab0d")
        tools.replace_in_file("SPIRV-Tools/CMakeLists.txt", "project(spirv-tools)", '''project(spirv-tools)
            include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
            conan_basic_setup()'''
        )

    def requirements(self):
        self.requires.add("SPIRV-Headers/ac638f18", private=False)

    def build(self):
        cmake = CMake(self)
        spirv_headers_dir = '{0}/..'.format(self.deps_cpp_info["SPIRV-Headers"].include_paths[0])

        cmake_linker_flags = ""
        if self.options.lto == True:
            cmake_linker_flags += " -fuse-ld=gold -fuse-linker-plugin "
            cmake.definitions["CMAKE_INTERPROCEDURAL_OPTIMIZATION"] = "TRUE"

        if not cmake_linker_flags:
            cmake.definitions["CMAKE_EXE_LINKER_FLAGS"] = cmake_linker_flags

        cmake.definitions["SPIRV-Headers_SOURCE_DIR"] = spirv_headers_dir
        cmake.definitions["SPIRV_SKIP_EXECUTABLES"] = 'ON'
        cmake.definitions["SPIRV_WERROR"] = 'OFF'
        cmake.configure(source_folder="SPIRV-Tools")
        cmake.build()
        cmake.install()

    def package(self):
        # required for glslang package
        self.copy("message.h", dst="include", src="SPIRV-Tools/source")

    def package_info(self):
        self.cpp_info.libs = ["SPIRV-Tools-link", "SPIRV-Tools-opt", "SPIRV-Tools"]
        self.cpp_info.libdirs = ['lib', 'lib64']
