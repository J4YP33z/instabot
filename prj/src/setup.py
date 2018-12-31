from cx_Freeze import setup, Executable

setup(
    name="bot",
    options = {"build_exe": {"packages":["idna", "requests"]}},
    version="0.1",
    description="",
    executables=[
        Executable("bot.py"),
    ],
)
