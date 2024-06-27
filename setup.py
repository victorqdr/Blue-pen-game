import cx_Freeze
executables = [cx_Freeze.Executable(
    script="main.py", icon="recursos/icone.png")]

cx_Freeze.setup(
    name="Blue pen the game",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": ["recursos"]
                           }},
    executables=executables
)