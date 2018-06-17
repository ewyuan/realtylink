from setuptools import setup

setup(name='realtylink',
      version='1.0',
      author='Eric Yuan',
      packages=['realtylink'],
      install_requires=[
            'schedule',
            'pandas',
            'requests',
            'lxml']
      )
