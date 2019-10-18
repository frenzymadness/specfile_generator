import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

print(setuptools.find_packages())

setuptools.setup(
    name="specfile_generator",
    version="0.0.0-dev",
    author="Lumir Balhar",
    author_email="author@example.com",
    description="Project trying to automate making specfiles from pypi packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frenzymadness/specfile_generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.6',
    zip_safe=True,
    license_files="LICENSE",
    package_data={
            'gen_spec': ['*spec'],
        }
)

