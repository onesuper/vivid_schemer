from setuptools import setup

from vivid_schemer import __version__, __github__

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='vivid_schemer',
    version=str(__version__),
    author='onesuper',
    author_email='onesuperclark@gmail.com',
    packages=['vivid_schemer', 'vivid_schemer/playbook'],
    entry_points={
        'console_scripts': 'vivid_schemer = vivid_schemer.playbook.cli:cli'
    },
    url=str(__github__),
    license='MIT',
    description='REPL for The Little Schemer',
    install_requires=required,
    test_suite='nose.collector',
    tests_require=['nose'],
    include_package_data=True,
    zip_safe=False
)
