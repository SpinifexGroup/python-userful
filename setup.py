#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_reqs = [
    'requests',
]

test_requirements = [
    'pytest-cov',
]

with open('README.md') as f:
    readme = f.read()

setup(
        name='userful',
        version='0.1.0',
        description='Unofficial python client for userful API',
        long_description=readme,
        long_description_content_type='text/markdown',
        author='Spinifex Group',
        author_email='justin.crown@spinifexgroup.com',
        url='https://github.com/SpinifexGroup/python-userful',
        packages=[
            'userful'
        ],
        package_dir={'userful': 'userful'},
        tests_require=test_requirements,
        install_requires=install_reqs,
        license='MIT',
        zip_safe=False,
        keywords='userful',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Programming Language :: Python :: 3',
        ],
)
