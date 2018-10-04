"""
Main entry point for executing the PythonTurtle application.

We need an absolute import here for PyInstaller to work.
See https://github.com/pyinstaller/pyinstaller/issues/2560
"""
from pythonturtle import application

if __name__ == "__main__":
    application.run()
