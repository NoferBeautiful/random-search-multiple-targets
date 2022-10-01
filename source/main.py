from grid import Grid
from point import Point


def search(point, grid, canvas=None):
    found_x = False
    found_y = False
    while True:
        check = grid.check(*point.get_point())
        if check == 3:
            break
        elif check == 2 and not found_y:
            point.change_y_distribution("end")
            found_y = True
        elif check == 3 and not found_x:
            point.change_x_distribution("end")
            found_x = True
        point.move()
        point.draw_dot(canvas)
        grid.draw(canvas)
