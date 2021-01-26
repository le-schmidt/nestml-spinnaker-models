import os
from setuptools import setup
from collections import defaultdict

__version__ = None
exec(open("python_models8/_version.py").read())
assert __version__


# Build a list of all project modules, as well as supplementary files
main_package = "python_models8"
extensions = {".aplx", ".boot", ".cfg", ".json", ".sql", ".template", ".xml",
              ".xsd"}
main_package_dir = os.path.join(os.path.dirname(__file__), main_package)
start = len(main_package_dir)
packages = []
package_data = defaultdict(list)
for dirname, dirnames, filenames in os.walk(main_package_dir):
    if '__init__.py' in filenames:
        package = "{}{}".format(
            main_package, dirname[start:].replace(os.sep, '.'))
        packages.append(package)
    for filename in filenames:
        _, ext = os.path.splitext(filename)
        if ext in extensions:
            package = "{}{}".format(
                main_package, dirname[start:].replace(os.sep, '.'))
            package_data[package].append(filename)

url = "https://github.com/SpiNNakerManchester/sPyNNaker8NewModelTemplate"

setup(
    name="sPyNNaker8NewModelTemplate",
    version=__version__,
    description="SpiNNaker 8 Template for New Models",
    url=url,
    classifiers=[
        "Development Status :: 3 - Alpha",

        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Natural Language :: English",

        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",

        "Programming Language :: C",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=packages,
    package_data=package_data,
    install_requires=[
        'SpiNNUtilities >= 1!5.1.1, < 1!6.0.0',
        'SpiNNMachine >= 1!5.1.1, < 1!6.0.0',
        'SpiNNMan >= 1!5.1.1, < 1!6.0.0',
        'SpiNNaker_PACMAN >= 1!5.1.1, < 1!6.0.0',
        'SpiNNaker_DataSpecification >= 1!5.1.1, < 1!6.0.0',
        'spalloc >= 2.0.2, < 3.0.0',
        'SpiNNFrontEndCommon >= 1!5.1.1, < 1!6.0.0',
        'sPyNNaker >= 1!5.1.1, < 1!6.0.0',
        'sPyNNaker8 >= 1!5.1.1, < 1!6.0.0'],
    maintainer="SpiNNakerTeam",
    maintainer_email="spinnakerusers@googlegroups.com"
)
