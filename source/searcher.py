class Searcher:
    def __init__(self, point, grid, scene, UI):
        self.__point = point
        self.__grid = grid
        self.__scene = scene
        self.__found_x = False
        self.__found_y = False
        self.__UI = UI

    def restart(self):
        self.__found_x = False
        self.__found_y = False

    def end(self):
        self.__UI.pause()

    def search(self):
        self.__point.move()
        check = self.__grid.check(*self.__point.get_point(), self.__scene)
        if check == 3:
            self.end()
        elif check == 2 and not self.__found_y:
            self.__point.change_y_distribution("end")
            self.__found_y = True
        elif check == 1 and not self.__found_x:
            self.__point.change_x_distribution("end")
            self.__found_x = True
