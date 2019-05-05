from setuptools import setup
from setuptools import find_packages

setup(name='vmspider',
      version='0.1',
      description='The best spider in the world',
      url='http://github.com/vmouta/vmspider',
      author='Vasco Mouta',
      author_email='vasco.mouta@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={'scrapy': ['settings = vmspider.settings'] ,
                    'console_scripts': ['vmspider = vmspider.__main__:main']},
      zip_safe=False)