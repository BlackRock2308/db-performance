from setuptools import setup, find_packages

setup(
    name='dbperf',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pyspark>=3.1.2',
        'pytest',
        # Add other dependencies here
    ],
    python_requires='>=3.8',
    author='JoyBoy',
    description='Data Processing Spark Job',
)