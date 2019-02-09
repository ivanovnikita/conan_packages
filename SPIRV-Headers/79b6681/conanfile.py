from conans import ConanFile, tools
import os


class SpirvheadersConan(ConanFile):
    name = "SPIRV-Headers"
    version = "79b6681"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Spirvheaders here>"
    no_copy_source = True
    # No settings/options are necessary, this is header only

    def source(self):
        self.run("git clone https://github.com/KhronosGroup/SPIRV-Headers.git")
        self.run("cd SPIRV-Headers && git checkout 79b6681")

    def package(self):
        self.copy("*", dst="include", src="SPIRV-Headers/include")
