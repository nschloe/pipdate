import os
import sys

from setuptools import find_packages, setup

# https://packaging.python.org/single_source_version/
base_dir = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(base_dir, "pipdate", "__about__.py"), "rb") as f:
    exec(f.read(), about)


setup(
    name="pipdate",
    version=about["__version__"],
    packages=find_packages(),
    url="https://github.com/nschloe/pipdate",
    author=about["__author__"],
    author_email=about["__email__"],
    install_requires=["appdirs", "requests"],
    description="pip update helpers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license=about["__license__"],
    classifiers=[
        about["__status__"],
        about["__license__"],
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "Topic :: Software Development :: Version Control",
        "Topic :: System :: Software Distribution",
    ],
    entry_points={
        "console_scripts": [
            "{} = pipdate.cli:update".format(
                "pipdate" if sys.version_info[0] < 3 else "pipdate3"
            )
        ]
    },
)
