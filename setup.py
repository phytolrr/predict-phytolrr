import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="predict-phytolrr",
    version="2020.11dev1",
    author="PhytoLRR",
    author_email="phytolrr@163.com",
    description="A tool which predict phyto-LRRs from a sequences.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phytolrr/predict-phytolrr",
    py_modules=['predict_phytolrr'],
    packages=setuptools.find_packages(include=['phytolrr_predictor', 'phytolrr_predictor.*']),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    install_requires=[
        'biopython>=1.73,<1.78',
        'numpy>=1.16.3'
    ],
    package_data={
        "phytolrr_predictor.resources": ["*.html"]
    },
    entry_points={
        'console_scripts': [
            'predict-phytolrr=predict_phytolrr:main',
        ],
    },
)

# python3 setup.py sdist bdist_wheel