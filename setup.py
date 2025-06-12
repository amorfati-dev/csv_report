"""Setup configuration for csv_report package."""
from setuptools import setup, find_packages

setup(
    name="csv_report",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=2.0.0",
        "jinja2>=3.0.0",
        "yagmail>=0.15.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
        ],
    },
    python_requires=">=3.8",
) 