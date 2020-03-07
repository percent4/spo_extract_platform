# build script for 'dvedit' - Python libdv wrapper

# change this as needed
# libdvIncludeDir = "/usr/include/libdv"

import sys, os
from distutils.core import setup
from distutils.extension import Extension

os.chdir(os.path.dirname(__file__))

# we'd better have Cython installed, or it's a no-go
try:
    from Cython.Distutils import build_ext
except Exception as e:
    print("You don't seem to have Cython installed. Please get a")
    print("copy from www.cython.org and install it")
    sys.exit(1)

SRC_DIR = "src"

def scandir(dir, files=[]):
    for file in os.listdir(dir):
        path = os.path.join(dir, file)
        if 'thirdparty' in file:
            continue
        if '__init__' in file:
            continue
        if 'run' in file:
            continue
        if os.path.isfile(path) and path.endswith(".py"):
            files.append(path.replace(os.path.sep, ".")[:-3])
        elif os.path.isdir(path):
            scandir(path, files)
    return files


def make_extension(extName):
    extPath = extName.replace(".", os.path.sep) + ".py"
    return Extension(extName, [extPath], include_dirs=["."])

def get_packages(folder, packages=[]):
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isdir(path) and os.path.exists(
                '{}/__init__.py'.format(path)):
            packages.append(path)
            get_packages(path, packages)
    packages.append(folder)
    return [p.replace('/', '.') for p in packages]


def clean(target_dir):
    if 'thirdparty' not in target_dir:
        for file in os.listdir(target_dir):
            path = os.path.join(target_dir, file)
            if os.path.isfile(path) and 'run' not in file:
                os.system("rm {}".format(path))
            elif os.path.isdir(path) and 'bert' not in path and 'chinese_L-12' not in path \
                    and 'ckpt' not in path and 'data' not in path and 'log' not in path:
                clean(path)

def copy_so(target_dir, build_base_dir, taget_base_dir):
    for file in os.listdir(target_dir):
        path = os.path.join(target_dir, file)
        if os.path.isfile(path) and path.endswith(".so"):
            new_path = path.replace(build_base_dir, taget_base_dir)
            os.system("cp {} {}".format(path, new_path))
        elif os.path.isdir(path):
            copy_so(path, build_base_dir, taget_base_dir)


def get_build_base_dir():
    for file in os.listdir('build'):
        if file[:3] == 'lib':
            return 'build/{}/{}'.format(file, 'src')


ext_names = scandir(SRC_DIR)
extensions = [make_extension(name) for name in ext_names]
packages = get_packages(SRC_DIR)
print(packages)
setup(
    name="src",
    packages=packages,
    ext_modules=extensions,
    cmdclass={'build_ext': build_ext}, )
clean(SRC_DIR)
build_base_dir = get_build_base_dir()
copy_so(build_base_dir, build_base_dir, SRC_DIR)
os.system('rm -rf build')