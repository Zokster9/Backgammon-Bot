from colorama import init, Fore, Back, Style

init(autoreset=True)


class BlackFigure:
    @staticmethod
    def figure():
        return Style.BRIGHT + Back.BLACK + Fore.WHITE + "O" + Style.RESET_ALL


class WhiteFigure:
    @staticmethod
    def figure():
        return Style.BRIGHT + Back.WHITE + Fore.BLACK + "O" + Style.RESET_ALL
