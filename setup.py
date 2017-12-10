from setuptools import setup
long_description = open('README.rst').read()

setup(
    name='pySOTDashboard',
    version='0.1.0',
    packages=['pySOTDashboard', 'pySOTDashboard.test'],
    url='https://github.com/peiyu313/pySOTDashboard',
    license='LICENSE.rst',
    author='Israr Mahmood, Peiyu Shi',
    author_email='im278@cornell.edu, ps735@cornell.edu',
    description='pySOT Web Dashboard',
    long_description=long_description,
    setup_requires=['numpy'],
    install_requires=['scipy',
                      'pyDOE',
                      'POAP>=0.1.25',
                      'py_dempster_shafer',
                      'flask',
                      'flask-socketio'],
    classifiers=['Intended Audience :: Science/Research',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Operating System :: Unix',
                 'Operating System :: MacOS',
                 ]
)
