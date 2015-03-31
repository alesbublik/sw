from setuptools import setup
from os.path import join


setup(
    name="sw",
    version="0.1",
    py_modules=['sw'],
    author="Ales Bublik",
    author_email="ales@bublik.eu",
    license="MIT",
    keywords="batch parser",
    url="",
    description="",
    download_url="",
    install_requires=['opterator'],
    scripts=[join("bin", "sw")],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
