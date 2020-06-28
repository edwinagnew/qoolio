import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qoolio-edwinagnew", # Replace with your own username
    version="0.0.5",
    author="Edwin Agnew",
    author_email="edwinagnew1@gmail.com",
    description="A (handy) collection of miscellaneous quantum gizmos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edwinagnew/qoolio",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
