from setuptools import setup
setup(
    name='Brainfried',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'brainfry=brainfry:main'
        ]
    }
)
