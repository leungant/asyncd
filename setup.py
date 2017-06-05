from setuptools import setup

setup(name='asyncd',
      version='1.39',
      description='Cool yet simple async for Python 3 and 2',
      url='http://github.com/leungant/asyncd',
      author='Anthony Leung',
      author_email='anthony.leung@gmail.gm',
      license='MIT',
      packages=['asyncd'],
      install_requires=[
          'pylru',
      ],
      zip_safe=False)
