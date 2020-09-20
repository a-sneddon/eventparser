import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="eventparser",
    version="1.0",
    author="Alex Sneddon",
    author_email="Alexandra.Sneddon@anu.edu.au",
    description="A package to parse eventalign files produced by Nanopolish to an intermediate data format, to improve the ease of downstream processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a-sneddon/eventparser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)