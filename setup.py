# setup.py
from pathlib import Path
from setuptools import find_namespace_packages, setup

BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

#Define facebook package
setup(
    name = "src",
    version=0.1,
    description='Cooking recipe recommendation',
    python_requires=">=3.8",
    packages=find_namespace_packages(),
    install_requires=[required_packages]
)