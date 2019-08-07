from conans import ConanFile, CMake, tools
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class LuaConan(ConanFile):
    name = "Lua"
    version = "5.3.5"
    description = "Lua is a powerful, fast, lightweight, embeddable scripting language."
    # topics can get used for searches, GitHub topics, Bintray tags etc. Add here keywords about the library
    topics = ("conan", "lua", "scripting", "embedded")
    url = "https://github.com/helmesjo/conan-lua"
    homepage = "https://www.lua.org"
    author = "helmesjo <helmesjo@live.com>"
    license = "MIT"  # Indicates license type of the packaged library; please use SPDX Identifiers https://spdx.org/licenses/
    exports = ["LICENSE.md"]      # Packages the license for the conanfile.py
    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    requires = ()

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://www.lua.org"
        tools.get("{0}/ftp/lua-{1}.tar.gz".format(source_url, self.version), sha256="0c2eed3f960446e1a3e4b9a1ca2f3ff893b6ce41942cf54d5dd59ab4b3b058ac")
        extracted_dir = "lua-" + self.version

        # Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):        
        cmake = CMake(self)
        cmake.definitions["SOURCE_SUBDIR"] = self._source_subfolder
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
