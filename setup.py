from setuptools import setup, find_packages

setup(
    name="trading-bot",
    version="1.0.0",
    description="Trading Bot for Binance Futures Testnet",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "trading-bot=cli:main",
        ],
    },
)