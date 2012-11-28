from distutils.core import setup

PACKAGE = "paymo"
NAME = "paymo"
DESCRIPTION = "Python wrapper for the Paymo API."
AUTHOR = "Paulo Scardine"
AUTHOR_EMAIL = "paulo@xtend.com.br"
URL = "http://packages.python.org/paymo"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open("README.TXT").read(),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages = ['paymo',],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Software Development :: Libraries",
    ],
    zip_safe=False,
)
