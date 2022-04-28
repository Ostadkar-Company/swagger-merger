import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swagger-merger",
    version="1.2.0",
    author="Sina Mehrabi",
    description="swagger merger python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,

    url='https://github.com/ostadkarteam/swagger-merger',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["swagger_merger"],
    package_dir={'./': 'swagger_merger/src'},
    install_requires=["deepmerge", "PyYAML"],
    entry_points={
        'console_scripts': [
            'merger = swagger_merger.src.cli:main'
        ]
    },
)
