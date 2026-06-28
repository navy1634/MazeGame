from app.lib.set_log import logger_conf
from app.app import App


def main() -> None:
    logger = logger_conf()
    app = App()
    app.run()


if __name__ == "__main__":
    main()
