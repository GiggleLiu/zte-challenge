'''
Set up file for matrix product state.
'''
def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config=Configuration('',parent_package,top_path)
    config.add_extension('binpacking',['binpacking.f90'],libraries=[])
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(configuration=configuration)
