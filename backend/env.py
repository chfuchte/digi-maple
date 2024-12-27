import sys

def is_docker():
    # check if --docker flag is passed
    if "--docker" in sys.argv:
        return True
    return False
