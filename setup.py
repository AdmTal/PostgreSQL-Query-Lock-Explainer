import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    'prettytable',
    'psycopg2',
]

setuptools.setup(
    name="pg_explain_locks",  # Replace with your own username
    version="0.0.2",
    author="Adam Tal",
    author_email="admtal@gmail.com",
    description="Postgres utility to show what locks will be acquired by a given query.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdmTal/PostgreSQL-Query-Lock-Explainer",
    py_modules=['pg_explain_locks'],
    packages=setuptools.find_packages(),
    setup_requires=requirements,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pg_explain_locks = pg_explain_locks:main',
        ],
    },
    python_requires='>=3.6',
)
