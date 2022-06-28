from colorama import init, Fore, Back, Style

init(autoreset=True)


class Figures:
    @staticmethod
    def black_figure():
        return Style.BRIGHT + Back.BLACK + Fore.WHITE + "O" + Style.RESET_ALL

    @staticmethod
    def white_figure():
        return Style.BRIGHT + Back.WHITE + Fore.BLACK + "O" + Style.RESET_ALL
