from setuptools import setup

setup(
    name = 'qonic_misc',
    packages = ['qonic_misc'],
    version = '0.1.6',
    description = 'Python library with miscellaneous tools to be used in conjunction with the qonic framework',
    author = 'cogrpar',
    author_email = 'owen.r.welsh@hotmail.com',
    url = 'https://github.com/Qonic-Team/qonic-misc.git',
    download_url = 'https://github.com/Qonic-Team/qonic-misc/archive/refs/heads/main.zip',
    license='Apache License 2.0',
    keywords = ['qonic', 'qonic_misc'],
    setup_requires=['wheel'],
    install_requires=['numpy>=1.22.2 ', 'tensorflow>=2.12.0rc1', 'keras>=2.13.1rc0', 'setuptools>=65.5.1', 'werkzeug>=3.0.3', 'wheel>=0.38.0']
)
