from webbrowser import open
import os
import PATHS
react_path = os.path.join(PATHS.repository, "react-remake")
os.chdir(react_path)


if __name__ == "__main__":
    os.startfile(os.path.join(react_path, "runserver.bat"))
    open("http://localhost:5173/")