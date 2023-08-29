from setuptools import setup, find_packages

setup(
    name="AicfCardGenerator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.2.3",
        "pandas==1.5.1",
        "Pillow==9.3.0",
        "qrcode==7.4.2",
        "Requests==2.31.0",
        "selenium==4.11.2"
    ],
)
