import PyMisc.variable as var
import PyMisc.pattern as pt
import PyMisc.color as clr

if __name__ == '__main__':
    house: pt.Grid = pt.Grid(var.size(16, 29))

    ###############
    # Roof
    ###############
    roof: pt.Grid = pt.Grid(var.size(8, 29))

    # Top
    roof.draw_horizontal_line(
        char=var.char('='),
        position=var.position(0, 6),
        length=var.length(17),
        property_=clr.property(
            fg_color_code=clr.foreground.bright_cyan(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    # Roof borders
    roof.draw_diagonal_line_upward(                 ## Left ##
        char=var.char(')'),
        position=var.position(6, 0),
        length=var.length(6),
        property_=clr.property(
            fg_color_code=clr.foreground.cyan(),
            style_codes=[
                clr.style.bold(),
                clr.style.italic()
            ]
        )
    )
    roof.draw_diagonal_line_downward(                 ## Right ##
        char=var.char('('),
        position=var.position(1, 23),
        length=var.length(6),
        property_=clr.property(
            fg_color_code=clr.foreground.cyan(),
            style_codes=[
                clr.style.bold(),
                clr.style.italic()
            ]
        )
    )

    # Roof Fill
    for count in range(6):
        roof.draw_horizontal_line(
            char=var.char('V'),
            position=var.position(1 + count, 6 - count),
            length=var.length(9 + count),
            step=var.length(1),
            property_=clr.property(
                fg_color_code=clr.foreground.bright_magenta(),
                style_codes=[
                    clr.style.bold()
                ]
            )
        )

    # Bottom
    roof.draw_horizontal_line(
        char=var.char('~'),
        position=var.position(7, 0),
        length=var.length(29),
        property_=clr.property(
            fg_color_code=clr.foreground.red(),
            # bg_color_code=c.background.cyan(),
            style_codes=[
                clr.style.bold(),
                clr.style.italic()
            ]
        )
    )

    # roof.draw()

    ###############
    # Roof Room
    ###############
    roof_room: pt.Grid = pt.Grid(var.size(4, 7))

    # Top
    roof_room.insert_individual(
        char=var.char('^'),
        position=var.position(0, 3),
        property_=clr.property(
            fg_color_code=clr.foreground.green(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    roof_room.draw_horizontal_line(
        char=var.char('V'),
        position=var.position(0, 1),
        length=var.length(2),
        step=var.length(3),
        property_=clr.property(
            fg_color_code=clr.foreground.bright_magenta(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=var.char('/'),
        position=var.position(0, 2),
        property_=clr.property(
            fg_color_code=clr.foreground.green(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=var.char('/'),
        position=var.position(1, 0),
        property_=clr.property(
            fg_color_code=clr.foreground.green(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=var.char('\\'),
        position=var.position(0, 4),
        property_=clr.property(
            fg_color_code=clr.foreground.green(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=var.char('\\'),
        position=var.position(1, 6),
        property_=clr.property(
            fg_color_code=clr.foreground.green(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=var.char('_'),
        position=var.position(1, 3),
        property_=clr.property(
            fg_color_code=clr.foreground.magenta(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=var.char('#'),
        position=var.position(2, 3),
        property_=clr.property(
            fg_color_code=clr.foreground.bright_blue(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=var.char('~'),
        position=var.position(3, 3),
        property_=clr.property(
            fg_color_code=clr.foreground.red(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    roof_room.draw_horizontal_line(
        char=var.char('|'),
        position=var.position(2, 0),
        length=var.length(4),
        step=var.length(1),
        property_=clr.property(
            fg_color_code=clr.foreground.green(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    roof_room.draw_horizontal_line(
        char=var.char('|'),
        position=var.position(3, 0),
        length=var.length(2),
        step=var.length(5),
        property_=clr.property(
            fg_color_code=clr.foreground.green(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    # roof_room.draw()

    roof.insert_grid(
        position=var.position(3, 11),
        grid_=roof_room,
        remove_bg_mode=False
    )

    # roof.draw()

    ###############
    # Body
    ###############
    body: pt.Grid = pt.Grid(var.size(8, 29))

    body.draw_filled_box(
        char=var.char(':'),
        position=var.position(0, 0),
        size=var.size(8, 29),
        property_=clr.property(
            fg_color_code=clr.foreground.bright_yellow(),
            style_codes=[
                clr.style.bold(),
                clr.style.italic()
            ]
        )
    )

    ###############
    # Windows
    ###############
    window: pt.Grid = pt.Grid(var.size(3, 4))

    window.draw_filled_box(
        char=var.char('#'),
        position=var.position(0, 0),
        size=var.size(3, 4),
        property_=clr.property(
            fg_color_code=clr.foreground.bright_blue(),
            style_codes=[
                clr.style.bold(),
                clr.style.italic()
            ]
        )
    )

    window_large: pt.Grid = pt.Grid(var.size(3, 5))

    window_large.draw_filled_box(
        char=var.char('#'),
        position=var.position(0, 0),
        size=var.size(3, 5),
        property_=clr.property(
            fg_color_code=clr.foreground.bright_blue(),
            style_codes=[
                clr.style.bold(),
                clr.style.italic()
            ]
        )
    )

    # Inserting Windows
    window_positions: list[var.position] = [
        var.position(0, 5),
        var.position(4, 5),
        var.position(0, 20),
        var.position(4, 20),
    ]
    for position in window_positions:
        body.insert_grid(position=position, grid_=window)
    body.insert_grid(position=var.position(0, 12), grid_=window_large)

    ###############
    # Door
    ###############
    door: pt.Grid = pt.Grid(var.size(4, 5))

    for i in range(2):
        door.draw_vertical_line(
            char=var.char('I'),
            position=[var.position(0, 0), var.position(0, 4)][i],
            length=var.length(4),
            property_=clr.property(
                fg_color_code=clr.foreground.bright_magenta(),
                style_codes=[
                    clr.style.dim()
                ]
            )
        )

        door.draw_horizontal_line(
            char=[var.char('~'), var.char('_')][i],
            position=[var.position(0, 1), var.position(3, 1)][i],
            length=var.length(3),
            property_=clr.property(
                fg_color_code=clr.foreground.magenta(),
                style_codes=[
                    clr.style.dim()
                ]
            )
        )

    door.insert_individual(
        char=var.char(','),
        position=var.position(2, 1),
        property_=clr.property(
            fg_color_code=clr.foreground.bright_white(),
            style_codes=[
                clr.style.bold()
            ]
        )
    )

    # door.draw()

    body.insert_grid(
        position=var.position(4, 12),
        grid_=door,
        remove_bg_mode=False
    )

    # body.draw()

    ##############################
    # Inserting parts
    ##############################
    house.insert_grid(var.position(0, 0), roof)       # Roof
    house.insert_grid(var.position(8, 0), body)       # Body


    house.draw()

    # Text
    text: pt.Grid = pt.Grid(var.size(1, 29))

    text.insert_text(
        position=var.position(0, 8),
        text=var.constant('Talha\'s House'),
        property_=clr.property(
            fg_color_code=clr.foreground.bright_blue(),
            bg_color_code=clr.background.black()
        )
    )

    text.draw()
