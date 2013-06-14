from setuptools import setup, find_packages

setup(
    name="yunomi",
    version="0.3.0",
    description="A Python metrics library with rate, statistical distribution, and timing information.",
    maintainer="David Reid",
    maintainer_email="dreid@dreid.org",
    url="https://github.com/dreid/yunomi",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",

    ],
    packages=find_packages()
)
