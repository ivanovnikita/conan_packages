from conans import ConanFile, tools
import os


class SpirvheadersConan(ConanFile):
    name = "SPIRV-Headers"
    version = "204cd13"
    no_copy_source = True
    # No settings/options are necessary, this is header only

    def source(self):
        self.run("git clone https://github.com/KhronosGroup/SPIRV-Headers.git")
        self.run("cd SPIRV-Headers && git checkout 204cd13")

    def package(self):
        self.copy("*", dst="include", src="SPIRV-Headers/include")
