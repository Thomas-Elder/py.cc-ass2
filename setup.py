from setuptools import find_packages, setup

setup(
    name='music',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'boto3==1.17.110',
        'botocore==1.20.110',
        'click==8.0.1',
        'colorama==0.4.4',
        'Flask==2.0.1',
        'Flask-WTF==0.15.1',
        'itsdangerous==2.0.1',
        'Jinja2==3.0.1',
        'jmespath==0.10.0',
        'MarkupSafe==2.0.1',
        'python-dateutil==2.8.1',
        's3transfer==0.4.2',
        'six==1.16.0',
        'urllib3==1.26.6',
        'waitress==2.0.0',
        'Werkzeug==2.0.1',
        'WTForms==2.3.3'
    ],
)