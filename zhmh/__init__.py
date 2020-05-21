import os


def get_path(save_path, name):
    return os.path.abspath(
        os.path.join(save_path, str(name))
    )




