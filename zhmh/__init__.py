import os
import matplotlib.pyplot as plt


def get_path(save_path, name):
    return os.path.abspath(
        os.path.join(save_path, str(name))
    )




