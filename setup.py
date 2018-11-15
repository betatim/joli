from distutils.core import setup

with open('README.md', encoding="utf8") as f:
    readme = f.read()

setup(
    name="joli",
    version="0.0.1",
    license='BSD',
    description="Joli notebooks",
    author="Tim Head",
    author_email="betatim@gmail.com",
    packages=["joli"],
    install_requires=["black"],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["joli = joli.app:main"]},
    long_description=readme,
    long_description_content_type='text/markdown',
    url='https://github.com/betatim/joli/',
    project_urls={
        'Documentation': 'https://github.com/betatim/joli/',
        'Source': 'https://github.com/betatim/joli/',
        'Tracker': 'https://github.com/betatim/joli/issues',
    },
)
