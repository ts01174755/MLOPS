import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_package",
    version="0.0.3",
    author="Author Name",
    author_email="ts01174755@gmail.com",
    description="Mlops",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ts01174755/MLOPS.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
