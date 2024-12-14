from setuptools import Extension, setup


def main():
    setup(
        name="cjson",
        version="1.0.0",
        author="Fedor Laputin",
        ext_modules=[Extension("cjson", ["cjson.c"])],
    )


if __name__ == "__main__":
    main()
