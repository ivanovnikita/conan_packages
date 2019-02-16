from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class XcbUtilWmConan(ConanFile):
    name = "xcb-util-wm"
    version = "0.4.1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of xcb-util-wm here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False]
        , "lto": [True, False]
    }
    default_options = {
        "shared": False
        , "lto": False
    }

    def source(self):
        tools.get(
            f"https://xcb.freedesktop.org/dist/{self.name}-{self.version}.tar.bz2"
        )

    def requirements(self):
        self.requires.add("xorg-util-macros/1.19.2@ivanovnikita/stable", private=False)
        self.requires.add("xcb/1.13.1@ivanovnikita/stable", private=False)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)

        if self.options.lto:
            autotools.flags.append("-flto")
            autotools.link_flags.append("-flto")
            autotools.link_flags.append("-fuse-ld=gold")
            autotools.link_flags.append("-fuse-linker-plugin")

        autotools.configure(
            configure_dir = f"{self.source_folder}/{self.name}-{self.version}"
            , pkg_config_paths = [
                f'''{self.deps_cpp_info["xorg-util-macros"].rootpath}/share/pkgconfig'''
                , f'''{self.deps_cpp_info["xcb"].rootpath}/share/pkgconfig'''
            ]
            , args = [
                "--disable-static" if self.options.shared else "--enable-static"
                , "--enable-shared" if self.options.shared else "--disable-shared"
                , "--disable-selective-werror"
                , "--disable-strict-compilation"
                , "--disable-devel-docs"
            ]
        )
        autotools.make()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["xcb-icccm", "xcb-ewmh"]
        self.cpp_info.libdirs = ['lib', 'lib64']