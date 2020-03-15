import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="predict-phytolrr-phytolrr",
    version="2020.03dev1",
    author="PhytoLRR",
    author_email="phytolrr@163.com",
    description="A tool which predict phyto-LRRs from a sequences.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phytolrr/predict-phytolrr",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    install_requires=[
        'biopython>=1.73'
    ],
    entry_points={
        'console_scripts': [
            'predict-phytolrr=predict_phytolrr:main',
        ],
    },
)
