from setuptools import setup

with open('README.rst','rb') as f:
    long_description = f.read().decode('utf-8')

setup(
    name='alug',
    version='1.0',
    description='wxPython components - list control and sizer utilities',
    long_description=long_description,
    url='https://github.com/AndersMunch/wxdo',
    author='Anders Munch',
    author_email='ajm@flonidan.dk',
    license='MIT',
    packages=['alug'],
    classifiers=[
        # 'Development Status :: 5 - Production/Stable',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Environment :: MacOS X :: Carbon',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: GTK',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Software Development :: User Interfaces ',
        'License :: OSI Approved :: BSD License',
        ],
    keywords='algorithms datastructures topological sort heap set heapset priority queue',
)