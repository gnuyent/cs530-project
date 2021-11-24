import toml
from gesture import gesture_use


def main():
    with open("config.toml", "r") as f:
        config = toml.load(f)

    print(config)
    gesture_use()


if __name__ == "__main__":
    main()
