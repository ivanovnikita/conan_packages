from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class XdmcpConan(ConanFile):
    name = "xcb"
    version = "1.13.1"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of xcb here>"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False]
        , "static_deps": [True, False]
        , "lto": [True, False]
        , "with_xinput": [True, False]
        , "with_xkb": [True, False]
    }
    default_options = {
        "shared": False
        , "static_deps": False
        , "lto": False
        , "with_xinput": False
        , "with_xkb": False
    }

    def source(self):
        tools.get(
            f"https://xcb.freedesktop.org/dist/libxcb-{self.version}.tar.bz2"
        )

    def requirements(self):
        self.requires.add("xorg-util-macros/1.19.2@ivanovnikita/stable", private=False)
        self.requires.add("xorgproto/2018.4@ivanovnikita/stable", private=False)
        self.requires.add("xau/1.0.8@ivanovnikita/stable", private=False)
        self.requires.add("xdmcp/1.1.2@ivanovnikita/stable", private=False)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)

        if self.options.static_deps:
            autotools.link_flags.append("-static")

        if self.options.lto:
            autotools.flags.append("-flto")
            autotools.link_flags.append("-flto")
            autotools.link_flags.append("-fuse-ld=gold")
            autotools.link_flags.append("-fuse-linker-plugin")

        autotools.configure(
            configure_dir = f"{self.source_folder}/libxcb-{self.version}"
            , pkg_config_paths = [
                f'''{self.deps_cpp_info["xorg-util-macros"].rootpath}/share/pkgconfig'''
                , f'''{self.deps_cpp_info["xorgproto"].rootpath}/share/pkgconfig'''
                , f'''{self.deps_cpp_info["xau"].rootpath}/lib/pkgconfig'''
                , f'''{self.deps_cpp_info["xdmcp"].rootpath}/lib/pkgconfig'''
            ]
            , args = [
                "--disable-static" if self.options.shared else "--enable-static"
                , "--enable-shared" if self.options.shared else "--disable-shared"
                , "--enable-xinput" if self.options.with_xinput else "--disable-xinput"
                , "--enable-xkb" if self.options.with_xkb else "--disable-xkb"
                , "--disable-selective-werror"
                , "--disable-strict-compilation"
                , "--disable-devel-docs"
                , "--disable-composite"
                , "--disable-damage"
                , "--disable-dpms"
                , "--disable-dri2"
                , "--disable-dri3"
                , "--disable-ge"
                , "--disable-glx"
                , "--disable-present"
                , "--disable-randr"
                , "--disable-record"
                , "--disable-render"
                , "--disable-resource"
                , "--disable-screensaver"
                , "--disable-shape"
                , "--disable-shm"
                , "--disable-sync"
                , "--disable-xevie"
                , "--disable-xfixes"
                , "--disable-xfree86-dri"
                , "--disable-xinerama"
                , "--disable-xprint"
                , "--disable-selinux"
                , "--disable-xtest"
                , "--disable-xv"
                , "--disable-xvmc"
            ]
        )
        autotools.make()
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["xcb"]

        if self.options.with_xinput:
            self.cpp_info.libs.append("xinput")

        if self.options.with_xkb:
            self.cpp_info.libs.append("xkb")

        self.cpp_info.libdirs = ['lib', 'lib64']