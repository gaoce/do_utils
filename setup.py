from setuptools import setup, find_packages

setup(
    name="do-utils",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "python-digitalocean",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "do-utils=do_utils:cli"
        ]
    }
)
