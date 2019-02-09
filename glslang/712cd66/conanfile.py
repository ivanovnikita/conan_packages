from conans import ConanFile, CMake, tools


class GlslangConan(ConanFile):
    name = "glslang"
    version = "712cd66"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Glslang here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "lto": [True, False]}
    default_options = {"shared": False, "lto": False}
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/KhronosGroup/glslang.git")
        self.run("cd glslang && git checkout 712cd66")
        tools.replace_in_file("glslang/CMakeLists.txt", "project(glslang)", '''project(glslang)
            include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
            conan_basic_setup()'''
        )
        tools.replace_in_file("glslang/CMakeLists.txt", 
            '''if(NOT TARGET SPIRV-Tools-opt)
    set(ENABLE_OPT OFF)
endif()''', 
            ""
        )
        tools.replace_in_file("glslang/External/CMakeLists.txt", 
            "if(ENABLE_OPT AND NOT TARGET SPIRV-Tools-opt)", 
            "if(FALSE)"
        )
        tools.replace_in_file("glslang/SPIRV/CMakeLists.txt", 
            "target_link_libraries(SPIRV glslang SPIRV-Tools-opt)", 
            "target_link_libraries(SPIRV glslang SPIRV-Tools-opt SPIRV-Tools)"
        )

    def requirements(self):
        self.requires.add("SPIRV-Tools/df5bd2d@ivanovnikita/stable", private=False)

    def build(self):
        cmake = CMake(self)

        cmake_linker_flags = ""
        if self.options.lto == True:
            cmake_linker_flags += " -fuse-ld=gold -fuse-linker-plugin "
            cmake.definitions["CMAKE_INTERPROCEDURAL_OPTIMIZATION"] = "TRUE"

        if not cmake_linker_flags:
            cmake.definitions["CMAKE_EXE_LINKER_FLAGS"] = cmake_linker_flags
        
        cmake.configure(source_folder="glslang")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["glslang", "HLSL", "OGLCompiler", "OSDependent", "SPIRV", "SPVRemapper"]
        self.cpp_info.libdirs = ['lib', 'lib64']
