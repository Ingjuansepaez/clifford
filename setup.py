from setuptools import find_packages, setup
import glob 
import os

from glob import glob

package_name = 'clifford'

setup(
    name=package_name,
    version='0.0.0',
    packages=['clifford'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),

        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),

        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),

        (os.path.join('share', package_name), ['README.md']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jagger',
    maintainer_email='juansepc@hotmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'user_node = clifford.user:main',
        ],
    },
)