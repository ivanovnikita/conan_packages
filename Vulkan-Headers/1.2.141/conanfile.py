from conans import ConanFile, CMake, tools
import os


class VulkanheadersConan(ConanFile):
    name = "Vulkan-Headers"
    version = "1.2.141"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("git clone https://github.com/KhronosGroup/Vulkan-Headers.git")
        self.run("cd Vulkan-Headers && git checkout v1.2.141")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=f"{self.source_folder}/Vulkan-Headers")
        cmake.build()
        cmake.install()
