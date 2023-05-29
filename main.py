from src.delegators.app_delegator import AppDelegator


def main():
    AppDelegator() \
        .apply_config() \
        .apply_arguments() \
        .generate_pairs() \
        .generate_pictures() \


if __name__ == '__main__':
    main()
