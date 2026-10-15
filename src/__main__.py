from src import CLI
import fire


def main() -> None:
    try:
        fire.Fire(CLI)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
