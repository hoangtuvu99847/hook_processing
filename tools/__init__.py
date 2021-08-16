print('loader')

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

with open("config.yml", "r") as ymlfile:
    cfg = load(ymlfile, Loader=Loader)
