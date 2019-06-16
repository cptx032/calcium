from distutils.core import setup

setup(
    name='calcium',
    version='0.1.0',
    packages=['calcium'],
    description='A terminal game framework',
    author='Willie Lawrence',
    author_email='cptx032@gmail.com',
    url='https://github.com/cptx032/calcium/',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: Games/Entertainment',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only'
    ],
    install_requires=[
        'Pillow==5.0.0',
        'PyTweening==1.0.3'
    ],)
