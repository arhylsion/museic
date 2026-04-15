from setuptools import setup, find_packages

setup(
    name='museic',
    version='2.2.0-beta',
    packages=find_packages(),
    install_requires=[
        'pydub==0.25.1',
        'demucs==4.0.1',
        'librosa',
        'numpy',
        'diffq',
        'tqdm',
    ],
    entry_points='''
        [console_scripts]
        museic=museic.cli:main
    ''',
)