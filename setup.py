import platform
import setuptools

install_requires_list = [
    "requests==2.31.0",
    "pyyaml==6.0.1"
]

if platform.platform() == 'Windows':
    install_requires_list.append("windows-curses==2.3.2")

setuptools.setup(
    name="vargo",
    version="0.1",
    author="Baptiste GODEAU",
    author_email="baptiste.ge.godeau@gmail.com",
    description="Python visual interface to manage argocd from the terminal",
    url="https://github.com/Toast-arch/vargo",
    packages=['vargo'],
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=install_requires_list
)
