import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MoadeeB", # Replace with your own username
    version="2.0.1",
    author="Boštjan Gec",
    author_email="bostjan.gec@ijs.si",
    description="MoadeeB and Diofantos - exact equation discovery tools with application in OEIS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/B0Gec/Diofantos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = ["numpy", 
                        "pandas", 
                        "scipy", 
                        "sympy", 
                        "nltk",
                        # "scikit-learn",
                        "hyperopt",
                        "diophantine",
                        "pytest",
                       ]
)
