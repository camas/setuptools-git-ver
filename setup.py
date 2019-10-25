import setuptools
from setuptools_git_ver import version_from_git

with open('readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="setuptools-git-ver",
    version=version_from_git(),
    author="Camas",
    author_email="camas@hotmail.co.uk",
    description="Automatically set package version using git tag/hash",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/camas/setuptools-git-ver",
    keywords='setuptools git version-control',
    packages=setuptools.find_packages(),
    classifiers=[
        'Framework :: Setuptools Plugin',
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    py_modules=['setuptools_git_ver'],
    install_requires=['setuptools'],
    entry_points={
        'distutils.setup_keywords': [
            'version_config = setuptools_git_ver:parse_config'
        ],
    },
)
