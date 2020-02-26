from setuptools import setup, find_packages

setup(
    name='webserver',
    version="2.0.0",
    description="webserver: Server-side endpoints for 0x2048",
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        "web3>=5.4.0,<6",
    ],
)
