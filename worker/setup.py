from setuptools import setup, find_packages

setup(
    name='block-chain-worker',
    version='0.1',
    packages = ['client'],
    include_package_data=True,
    install_requires=[
        'websockets',
        'requests',
        'click',
        'sqlalchemy',
        'psycopg2-binary'
    ],
    entry_points='''
        [console_scripts]
        block-chain-worker=client.main:cli
    ''',
)