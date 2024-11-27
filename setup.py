from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="volleyball_system",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive Flask-based volleyball team management system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/volleyball_system",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Sports Teams",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'pytest-flask>=1.2',
            'pytest-env>=0.6',
            'black>=21.0',
            'flake8>=3.9',
            'mypy>=0.900',
            'isort>=5.9',
        ],
        'test': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'pytest-flask>=1.2',
            'pytest-env>=0.6',
        ],
        'prod': [
            'gunicorn>=20.0',
            'psycopg2-binary>=2.9',
        ],
    },
    entry_points={
        'console_scripts': [
            'volleyball-system=run:main',
        ],
    },
    package_data={
        'app': [
            'static/**/*',
            'templates/**/*',
            'static/css/*',
            'static/js/*',
            'static/img/*',
            'static/profile_pics/*',
        ],
    },
    zip_safe=False,
)
