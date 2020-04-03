from conans import ConanFile, CMake, tools
import os


class VulkanvalidationlayersConan(ConanFile):
    name = "Vulkan-ValidationLayers"
    version = "1.2.133"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "with_xcb": [True, False]
    }
    default_options = {
        "with_xcb": False
    }
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/KhronosGroup/Vulkan-ValidationLayers.git")
        self.run("cd Vulkan-ValidationLayers && git checkout v1.2.133")
        
        tools.replace_in_file("Vulkan-ValidationLayers/CMakeLists.txt", 
            "project(Vulkan-ValidationLayers)", 
            '''project(Vulkan-ValidationLayers)
            include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
            conan_basic_setup()'''
        )

        tools.replace_in_file("Vulkan-ValidationLayers/layers/CMakeLists.txt", 
            '''-DRELATIVE_LAYER_BINARY="${RELATIVE_PATH_PREFIX}$<TARGET_FILE_NAME:${TARGET_NAME}>")''', 
            '''-DRELATIVE_LAYER_BINARY="${CMAKE_INSTALL_FULL_LIBDIR}/$<TARGET_FILE_NAME:${TARGET_NAME}>")'''
        )
        tools.replace_in_file("Vulkan-ValidationLayers/layers/CMakeLists.txt", 
            '''-DRELATIVE_LAYER_BINARY="$<TARGET_FILE_NAME:${TARGET_NAME}>")''', 
            '''-DRELATIVE_LAYER_BINARY="${CMAKE_INSTALL_FULL_LIBDIR}/$<TARGET_FILE_NAME:${TARGET_NAME}>")'''
        )

    def requirements(self):
        self.requires.add("Vulkan-Headers/1.2.133", private=False)
        self.requires.add("SPIRV-Tools/323a81f", private=False)
        self.requires.add("glslang/3ed344d", private=False)

        if self.options.with_xcb:
            self.requires.add("xcb/1.14", private=False)

    def build(self):
        cmake = CMake(self)

        cmake.definitions["GLSLANG_INSTALL_DIR"] = f'''{self.deps_cpp_info["glslang"].rootpath}'''
        cmake.definitions["SPIRV_TOOLS_BINARY_ROOT"] = f'''{self.deps_cpp_info["SPIRV-Tools"].rootpath}'''
        cmake.definitions["SPIRV_TOOLS_OPT_BINARY_ROOT"] = f'''{self.deps_cpp_info["SPIRV-Tools"].rootpath}'''

        cmake.definitions["BUILD_WSI_XLIB_SUPPORT"] = 'OFF'
        cmake.definitions["BUILD_WSI_WAYLAND_SUPPORT"] = 'OFF'
        if self.options.with_xcb:
            cmake.definitions["BUILD_WSI_XCB_SUPPORT"] = 'ON'
        else:
            cmake.definitions["BUILD_WSI_XCB_SUPPORT"] = 'OFF'

        cmake.definitions["BUILD_LAYERS"] = 'ON'
        cmake.definitions["BUILD_TESTS"] = 'OFF'
        cmake.configure(source_folder=f"{self.source_folder}/Vulkan-ValidationLayers")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = [
            "VkLayer_core_validation"
            , "VkLayer_object_lifetimes"
            , "VkLayer_thread_safety"
            , "VkLayer_unique_objects"
            , "VkLayer_stateless_validation"
        ]
        self.cpp_info.libdirs = ['lib', 'lib64']