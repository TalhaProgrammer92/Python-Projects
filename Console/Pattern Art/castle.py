import PyMisc.variable as var
import PyMisc.pattern as pt
import PyMisc.color as clr

def window() -> pt.Grid:
    _window: pt.Grid = pt.Grid(var.size(8, 14))

    # Box
    box: pt.Grid = pt.Grid(var.size(1, 2))
    box_color: clr.property = clr.property(
            fg_color_code=clr.foreground.bright_yellow(),
            style_codes=[
                clr.style.bold()
            ]
        )
    box.insert_individual(var.char('['), var.position(0, 0), box_color)
    box.insert_individual(var.char(']'), var.position(0, 1), box_color)

    # Borders - Vertical
    for count in range(8):
        _window.insert_grid(var.position(count, 0), box)
        _window.insert_grid(var.position(count, _window.width - 2), box)

    # Borders - Horizontal
    for count in range(0, 6 * 2, 2):
        _window.insert_grid(var.position(0, count), box)
        # print(var.position(0, count))
        _window.insert_grid(var.position(_window.height - 1, count), box)
        # print(var.position(_window.height - 1, count))

    return _window

if __name__ == '__main__':
    window().draw()
