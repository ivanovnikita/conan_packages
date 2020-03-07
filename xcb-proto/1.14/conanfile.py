from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class XcbProtoConan(ConanFile):
    name = "xcb-proto"
    version = "1.14"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "lto": [True, False]}
    default_options = {"shared": False, "lto": False}

    def source(self):
        tools.get(
            f"https://xcb.freedesktop.org/dist/xcb-proto-{self.version}.tar.gz"
        )

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)

        if self.options.lto:
            autotools.flags.append("-flto")
            autotools.link_flags.append("-flto")
            autotools.link_flags.append("-fuse-ld=gold")
            autotools.link_flags.append("-fuse-linker-plugin")

        autotools.configure(configure_dir = f"{self.source_folder}/xcb-proto-{self.version}")
        autotools.make()
        autotools.install()