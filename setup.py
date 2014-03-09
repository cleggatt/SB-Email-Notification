from distutils.core import setup, Command
import pytest

class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        errno = pytest.main()
        raise SystemExit(errno)
setup(
    name='sbnotify',
    version='1.0',
    packages=['sbnotify'],
    install_requires=[
        'httplib2',
        'pytest'
        ],
    cmdclass = {'test': PyTest}
)