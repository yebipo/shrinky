from distutils.core import setup

setup(name='Shrinky',
      version='1.0',
      description='Build small executables (dnload fork, for Arch Linux)', # dnload is here: https://github.com/faemiyah/dnload
      url='https://github.com/xyproto/shrinky',
      author='Alexander F. Rødseth',
      author_email='xyproto@archlinux.org',
      license="BSD",
      py_modules=["shrinky"],
      classifiers=[
          "Environment :: Console",
          "License :: OSI Approved :: BSD License", # New BSD license
          "Programming Language :: Python",
          "Topic :: System :: Shells",
          "Topic :: Utilities",
      ]
      )
