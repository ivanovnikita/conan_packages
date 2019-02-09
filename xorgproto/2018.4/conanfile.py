from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os


class XorgprotoConan(ConanFile):
    name = "xorgproto"
    version = "2018.4"
    license = "<Put the package license here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of xorgproto here>"
    settings = "os", "compiler", "build_type", "arch"

    def source(self):
        tools.get(
            f"https://xorg.freedesktop.org/archive/individual/proto/xorgproto-{self.version}.tar.bz2"
        )

    def requirements(self):
        self.requires.add("xorg-util-macros/1.19.2@ivanovnikita/stable", private=False)

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(
            configure_dir = f"{self.source_folder}/xorgproto-{self.version}"
            , pkg_config_paths = [f'''{self.deps_cpp_info["xorg-util-macros"].rootpath}/share/pkgconfig''']
            , args = [
                "--disable-selective-werror"
                , "--disable-strict-compilation"
                , "--disable-specs"
                , "--disable-legacy"
                , "--without-xmlto"
                , "--without-fop"
                , "--without-xsltproc"
            ]
        )
        autotools.make()
        autotools.install()
