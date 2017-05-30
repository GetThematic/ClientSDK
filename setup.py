
import setuptools


setuptools.setup(
    name = 'thematic_client_sdk',
    version = '1.0.0',
    author='Thematic Ltd',
    author_email='contact@getthematic.com',
    url='http://getthematic.com/',
    description = '',
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    entry_points = {
        'console_scripts': ['thematic-client-auth=thematic_client_sdk.scripts.interactive_auth:main'],
    }
)
