import pathlib

try:
    # Use setup() from setuptools(/distribute) if available
    from setuptools import setup
except ImportError:
    from distutils.core import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

from barqrcode import __version__

setup(
    name="barqrcode",
    version=__version__,
    # Your name & email here
    long_description=README,
    long_description_content_type="text/markdown",
    description="A program to take a number and print a number of bar or qr codes of it.",
    url="https://github.com/EricGebhart",
    author="Eric Gebhart",
    author_email="e.a.gebhart@gmail.com",
    packages=["barqrcode"],
    package_data={},
    scripts=[],
    license="MIT",
    entry_points={"console_scripts": ["barqrcode=barqrcode.__main__:main"]},
    install_requires=[
        "python-barcode",
        "qrcode",
        "pillow",
        "brother_ql",
    ],
)
