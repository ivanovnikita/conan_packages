from conans import ConanFile, CMake, tools
import os


class VulkanloaderConan(ConanFile):
    name = "Vulkan-Loader"
    version = "1.1.97"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Vulkan-Loader here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False]
        , "lto": [True, False]
        , "with_xcb": [True, False]
    }
    default_options = {
        "shared": False
        , "lto": False
        , "with_xcb": False
    }
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/KhronosGroup/Vulkan-Loader.git")
        self.run("cd Vulkan-Loader && git checkout v1.1.97")

        
        tools.replace_in_file("Vulkan-Loader/CMakeLists.txt", 
            "project(Vulkan-Loader)", 
            '''project(Vulkan-Loader)
            include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
            conan_basic_setup()'''
        )
        tools.replace_in_file("Vulkan-Loader/loader/CMakeLists.txt", 
            "add_library(vulkan SHARED", 
            "add_library(vulkan"
        )

    def requirements(self):
        self.requires.add("Vulkan-Headers/1.1.97@ivanovnikita/stable", private=False)

        if self.options.with_xcb:
            self.requires.add("xcb/1.13.1@ivanovnikita/stable", private=False)

    def build(self):
        cmake = CMake(self)

        cmake_linker_flags = ""
        if self.options.lto == True:
            cmake_linker_flags += " -fuse-ld=gold -fuse-linker-plugin "
            cmake.definitions["CMAKE_INTERPROCEDURAL_OPTIMIZATION"] = "TRUE"

        if not cmake_linker_flags:
            cmake.definitions["CMAKE_EXE_LINKER_FLAGS"] = cmake_linker_flags

        cmake.definitions["BUILD_WSI_XLIB_SUPPORT"] = 'OFF'
        cmake.definitions["BUILD_WSI_WAYLAND_SUPPORT"] = 'OFF'
        if self.options.with_xcb:
            cmake.definitions["BUILD_WSI_XCB_SUPPORT"] = 'ON'
        else:
            cmake.definitions["BUILD_WSI_XCB_SUPPORT"] = 'OFF'

        cmake.definitions["BUILD_LOADER"] = 'ON'
        cmake.definitions["BUILD_TESTS"] = 'OFF'
        cmake.configure(source_folder=f"{self.source_folder}/Vulkan-Loader")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["vulkan"]
        self.cpp_info.libdirs = ['lib', 'lib64']