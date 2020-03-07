from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class XorgUtilMacrosConan(ConanFile):
    name = "xorg-util-macros"
    version = "1.19.2"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        tools.get(
            f"https://xorg.freedesktop.org/releases/individual/util/util-macros-{self.version}.tar.bz2"
        )

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir = f"{self.source_folder}/util-macros-{self.version}")
        autotools.make()
        autotools.install()
