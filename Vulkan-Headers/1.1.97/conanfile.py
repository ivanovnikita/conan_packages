from conans import ConanFile, CMake, tools
import os


class VulkanheadersConan(ConanFile):
    name = "Vulkan-Headers"
    version = "1.1.97"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Vulkan-Headers here>"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        self.run("git clone https://github.com/KhronosGroup/Vulkan-Headers.git")
        self.run("cd Vulkan-Headers && git checkout v1.1.97")

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder=f"{self.source_folder}/Vulkan-Headers")
        cmake.build()
        cmake.install()
