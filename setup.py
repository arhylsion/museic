from setuptools import setup, find_packages

setup(
    name='museic',
    version='3.0.0',
    packages=find_packages(),
    install_requires=[
        'pydub==0.25.1',
        'demucs==4.0.1',
        'librosa',
        'numpy',
        'diffq',
        'tqdm',
        'watchdog',
        'gradio'
    ],
    extras_require={
        'dev': ['pytest'],
    },
    entry_points='''
        [console_scripts]
        museic=museic.cli:main
    ''',
)