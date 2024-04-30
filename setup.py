from setuptools import setup
#this will be needed and modified once creating the whole package

setup(
    name="Prolog-gym",
    version="0.0.1",
    install_requires=["gymnasium==0.28.1", "matplotlib==3.8.0", "pandas==2.1.4"],
    py_modules=['agents', 'env_input', 'norm_analysis']#,environments],
)
