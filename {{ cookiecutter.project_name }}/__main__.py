from config.logger import construct_logger
from config.settings import Settings

def main():
    settings = Settings()
    construct_logger(settings)
    return settings

    pass

if __name__ == "__main__":
    main()