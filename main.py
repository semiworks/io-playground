
import os
import sys


if __name__ == "__main__":
    # setup library lookup path before using it
    this_path = os.path.dirname(__file__)
    lib_path = os.path.join(this_path, 'libs')
    for d in os.listdir(lib_path):
        # create absolute path
        abs_path = os.path.join(lib_path, d)
        if os.path.isdir(abs_path):
            sys.path.append(abs_path)

    # run the application
    import app
    exit(app.run())
