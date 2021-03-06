from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=("tests",)),
    install_requires=[
        "attrs==21.4.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "click==8.0.4",
        "cycler==0.11.0; python_version >= '3.6'",
        "flask==2.0.2",
        "fonttools==4.29.1; python_version >= '3.7'",
        "gunicorn==20.1.0",
        "itsdangerous==2.1.0; python_version >= '3.7'",
        "jinja2==3.0.3; python_version >= '3.6'",
        "joblib==1.1.0; python_version >= '3.6'",
        "jsonschema==4.4.0",
        "kiwisolver==1.3.2; python_version >= '3.7'",
        "markupsafe==2.1.0; python_version >= '3.7'",
        "matplotlib==3.5.1",
        "numpy==1.22.2",
        "packaging==21.3; python_version >= '3.6'",
        "pillow==9.0.1; python_version >= '3.7'",
        "pyparsing==3.0.7; python_version >= '3.6'",
        "pyrsistent==0.18.1; python_version >= '3.7'",
        "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "scikit-learn==1.0.2",
        "scipy==1.8.0; python_version < '3.11' and python_version >= '3.8'",
        "setuptools==60.9.3; python_version >= '3.7'",
        "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "threadpoolctl==3.1.0; python_version >= '3.6'",
        "werkzeug==2.0.3; python_version >= '3.6'",
    ],
    test_suite="tests",
)
