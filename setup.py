from setuptools import find_packages, setup

package_name = 'odrive_projectile'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/odrive_projectile_launch.py']),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fennerco',
    maintainer_email='fennerco@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'dual_velocity = odrive_projectile.dual_odrive_velocity_control:main',
            'projectile_service = odrive_projectile.velocity_trigger_controller:main',
        ],
    },
)
