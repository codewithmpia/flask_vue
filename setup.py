from setuptools import setup, find_packages
import os

# Lire le README.md si disponible
readme_file = "README.md"
if os.path.exists(readme_file):
    try:
        with open(readme_file, "r", encoding="utf-8") as fh:
            long_description = fh.read()
    except Exception:
        long_description = "Flask-Vue - Extension Flask pour intégrer Vue 3, Vite et Tailwind CSS"
else:
    long_description = "Flask-Vue - Extension Flask pour intégrer Vue 3, Vite et Tailwind CSS"

setup(
    name="Flask-Vue3",
    version="0.1.1",
    author="codewithmpia",
    author_email="codewithmpia@gmail.com",
    description="Extension Flask pour intégrer Vue 3, Vite et Tailwind CSS 4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/codewithmpia/flask_vue",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "Flask>=2.0.0",
        "click>=8.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Flask",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.7",
    license="MIT",
    project_urls={
        "Bug Reports": "https://github.com/codewithmpia/flask_vue/issues",
        "Source": "https://github.com/codewithmpia/flask_vue",
    },
)