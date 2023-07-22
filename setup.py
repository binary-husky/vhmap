import setuptools, glob, os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

    
def _process_requirements():
    packages = open('requirements.txt').read().strip().split('\n')
    requires = []
    for pkg in packages:
        if pkg.startswith('git+ssh'):
            return_code = os.system('pip install {}'.format(pkg))
            assert return_code == 0, 'error, status_code is: {}, exit!'.format(return_code)
        else:
            requires.append(pkg)
    return requires

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('vhmap')



setuptools.setup(
    name="vhmap",
    version="4.0.0",
    author="Qingxu",
    author_email="505030475@qq.com",
    description="Advanced 3D visualizer for researchers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/binary-husky/vhmap",
    project_urls={
        "Bug Tracker": "https://github.com/binary-husky/vhmap/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    package_data={"": extra_files},
    include_package_data=True,
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
    install_requires=_process_requirements(),
)