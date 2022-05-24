from setuptools import setup


setup(
    name='snorrenapp',
    packages=['snorrenapp'],
    include_package_data=True,
    install_requires=[
        'flask',
        'mtcnn'
    ],
)
