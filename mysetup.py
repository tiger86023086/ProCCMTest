#my setup.py
from distutils.core import setup
import py2exe
import sys

sys.argv.append('py2exe')

py2exe_options={
      "includes":["PyQt5.sip",
                  "appdirs",
                  "packaging.specifiers",
                  "packaging.requirements",
                  "can.interfaces.canalystii"],
      "dll_excludes":["MSVCP90.dll",
                    "QT5CORE.DLL",
                    "PYTHON3.DLL",
                    "KERNEL32.DLL",
                    "VCRUNTIME140.DLL",],
      "compressed":1,
      "optimize":2,
      "ascii":0,
      "bundle_files":3,
      }
setup(
      name = 'MainTest',
      version = '1.0',
      windows = [{'script':'MainTest1.0.py','icon_resources':[(1,'car.ico')]}],
      #zipfile = None,
      options = {'py2exe':py2exe_options}
      )
#distutils.core.setup(windows=[{'script':'MainCreate.py','icon_resources':[(1,'timgCADXKVUY.ico')]}])