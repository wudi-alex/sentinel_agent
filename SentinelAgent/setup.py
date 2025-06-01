#!/usr/bin/env python3
"""
SentinelAgent Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text(encoding="utf-8").strip().split("\n")
    requirements = [req.strip() for req in requirements if req.strip() and not req.startswith("#")]

setup(
    name="sentinelagent",
    version="1.0.0",
    description="Advanced Agent System Analysis & Monitoring Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SentinelAgent Team",
    author_email="team@sentinelagent.dev",
    url="https://github.com/sentinelagent/sentinelagent",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sentinelagent=sentinelagent.cli.main:main",
            "sentinelagent-web=sentinelagent.cli.start_web_ui:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: System :: Monitoring",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    keywords="agent analysis monitoring security ai ml",
    project_urls={
        "Bug Reports": "https://github.com/sentinelagent/sentinelagent/issues",
        "Source": "https://github.com/sentinelagent/sentinelagent",
        "Documentation": "https://sentinelagent.readthedocs.io/",
    },
)
