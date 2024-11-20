from setuptools import setup, find_packages

setup(
    name='baseperf',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pyspark==3.1.2',
        'pytest'
    ],
    python_requires='>=3.8,<3.10'
)