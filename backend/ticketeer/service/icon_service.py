from injector import inject


class IconService():

    @inject
    def __init__(self) -> None:
        pass

    def icon_exists(self, id: int) -> bool:
        return True