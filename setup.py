from setuptools import setup, find_packages
import os

def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name), encoding='utf-8') as f:
        return f.read()

setup(
    name="check-swear",
    version="0.1.4",
    description="A profanity filter for Russian comments.",
    long_description=read('README.md'),  
    long_description_content_type="text/markdown",  
    author="Daniil Kremnev",
    author_email="legend.super567@gmail.com",
    packages=find_packages(exclude=["check_swear.tests", "check_swear.tests*"]),  # Exclude patterns adjusted
    include_package_data=True,
    package_data={
        'check_swear.data': ['*.joblib'],
        'check_swear.model_prep': ['*.json'],
    },
    install_requires=[
        "scikit-learn==1.4.0",
        "joblib==1.3.2",
        "nltk>=3.8.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)