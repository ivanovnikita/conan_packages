from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class MuslConan(ConanFile):
    name = "musl"
    version = "1.1.21"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of musl here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "lto": [True, False]}
    default_options = {"shared": False, "lto": False}

    def source(self):
        self.run("git clone git://git.musl-libc.org/musl")
        self.run(f"cd musl && git checkout v{self.version}")

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)

        if self.options.lto:
            autotools.flags.append("-flto")
            autotools.link_flags.append("-flto")
            autotools.link_flags.append("-fuse-ld=gold")
            autotools.link_flags.append("-fuse-linker-plugin")

        autotools.configure(
            configure_dir = f"{self.source_folder}/musl"
            , args = [
                "--disable-static" if self.options.shared else "--enable-static"
                , "--enable-shared" if self.options.shared else "--disable-shared"
                , "--disable-debug"
                , "--disable-warnings"
            ]
        )
        autotools.make()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = [
            "crypt"
            , "dl"
            , "m"
            , "pthread"
            , "resolv"
            , "rt"
            , "util"
            , "xnet"
            , "c"
        ]
        self.cpp_info.libdirs = ['lib', 'lib64']