from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="compiledUdl", 
    version="0.1.0",
    author="Tijin Saji",
    author_email="tijinsaji97@gmail.com",
    description="To compute excess chemical potential for highly polar and large molecules.",
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    url="https://github.com/tijinsaji/compile dUdl",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    # If your script requires other libraries (like requests, numpy, etc.), add them here:
    install_requires=[
        # "requests>=2.25.1", 
    ],
)
