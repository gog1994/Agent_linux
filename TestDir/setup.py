from cx_Freeze import setup, Executable

base = None

executables = [Executable("Testmodule.py",base=base)]

packages = ["idna"]
options = {
    'build_exe':{
	'packages' :packages,
	},
}

setup(
    name = "TestLog",
    options = options,
    version = "0.1",
    decription = 'test',
    executables = executables
)

