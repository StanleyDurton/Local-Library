import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="locallibrary", # Replace with your own username
    version="1.0.0",
    author="Stan",
    author_email="imaginistlu@outlook.com",
    description="Package for Library System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StanleyDurton/Local-Library.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)