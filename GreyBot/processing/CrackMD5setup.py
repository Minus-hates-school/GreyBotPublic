# setup.py
from Cython.Build import cythonize
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CustomBuildExt(build_ext):
    def build_extensions(self):
        # Force compiler executables here
        self.compiler.set_executable('compiler_so', 'C:/msys64/mingw64/bin/gcc.exe')
        self.compiler.set_executable('compiler_cxx', 'C:/msys64/mingw64/bin/g++.exe')
        self.compiler.set_executable('linker_so', 'C:/msys64/mingw64/bin/g++.exe')
        super().build_extensions()

setup(
    ext_modules=[Extension("CrackMd5.py", ["CrackMD5.pyx"])],
    cmdclass={'build_ext': CustomBuildExt},
)