from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="imageRuler",
    version="0.1.0",
    author="Adrien Bachelart",
    author_email="hello@adrienbc.com",
    url="https://github.com/adbac/imageRuler",
    license="MIT",
    description="A command-line tool that draws a height ruler next to the first page of a PDF, and outputs an image.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points="""
        [console_scripts]
        rule_image=ImageRuler.imageRuler:ruleImage
        rule_images=ImageRuler.imageRuler:ruleImages
        """,
    install_requires=[
        "click",
        "pypdf>=5.6.1",
    ],
    dependency_links=[
        "https://github.com/typemytype/drawbot",
        "https://github.com/mathieureguer/drawbotgrid",
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)