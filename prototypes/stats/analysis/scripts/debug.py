from analysis import run


def main():
    data = run()

    print(data)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
