from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(name='cosmicsense',
      version='0.0.1',
      description=u"Cosmic Ray Neutron Sensing",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"The cosmicsense organisation",
      author_email='heisterm@uni-potsdam.de',
      url='https://github.com/cosmic-sense/cosmicsense',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      extras_require={
          'test': ['pytest'],
      }
      )
