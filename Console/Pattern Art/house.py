import PyMisc.variable as v
import PyMisc.pattern as p
import PyMisc.color as c

if __name__ == '__main__':
    house: p.Grid = p.Grid(v.size(16, 29))

    ###############
    # Roof
    ###############
    roof: p.Grid = p.Grid(v.size(8, 29))

    # Top
    roof.draw_horizontal_line(
        char=v.char('='),
        position=v.position(0, 6),
        length=v.length(17),
        property_=c.property(
            fg_color_code=c.foreground.bright_cyan(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    # Roof borders
    roof.draw_diagonal_line_upward(                 ## Left ##
        char=v.char(')'),
        position=v.position(6, 0),
        length=v.length(6),
        property_=c.property(
            fg_color_code=c.foreground.cyan(),
            style_codes=[
                c.style.bold(),
                c.style.italic()
            ]
        )
    )
    roof.draw_diagonal_line_downward(                 ## Right ##
        char=v.char('('),
        position=v.position(1, 23),
        length=v.length(6),
        property_=c.property(
            fg_color_code=c.foreground.cyan(),
            style_codes=[
                c.style.bold(),
                c.style.italic()
            ]
        )
    )

    # Roof Fill
    for count in range(6):
        roof.draw_horizontal_line(
            char=v.char('V'),
            position=v.position(1 + count, 6 - count),
            length=v.length(9 + count),
            step=v.length(1),
            property_=c.property(
                fg_color_code=c.foreground.bright_magenta(),
                style_codes=[
                    c.style.bold()
                ]
            )
        )

    # Bottom
    roof.draw_horizontal_line(
        char=v.char('~'),
        position=v.position(7, 0),
        length=v.length(29),
        property_=c.property(
            fg_color_code=c.foreground.red(),
            # bg_color_code=c.background.cyan(),
            style_codes=[
                c.style.bold(),
                c.style.italic()
            ]
        )
    )

    # roof.draw()

    ###############
    # Roof Room
    ###############
    roof_room: p.Grid = p.Grid(v.size(4, 7))

    # Top
    roof_room.insert_individual(
        char=v.char('^'),
        position=v.position(0, 3),
        property_=c.property(
            fg_color_code=c.foreground.green(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    roof_room.draw_horizontal_line(
        char=v.char('V'),
        position=v.position(0, 1),
        length=v.length(2),
        step=v.length(3),
        property_=c.property(
            fg_color_code=c.foreground.bright_magenta(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=v.char('/'),
        position=v.position(0, 2),
        property_=c.property(
            fg_color_code=c.foreground.green(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=v.char('/'),
        position=v.position(1, 0),
        property_=c.property(
            fg_color_code=c.foreground.green(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=v.char('\\'),
        position=v.position(0, 4),
        property_=c.property(
            fg_color_code=c.foreground.green(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=v.char('\\'),
        position=v.position(1, 6),
        property_=c.property(
            fg_color_code=c.foreground.green(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=v.char('_'),
        position=v.position(1, 3),
        property_=c.property(
            fg_color_code=c.foreground.magenta(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=v.char('#'),
        position=v.position(2, 3),
        property_=c.property(
            fg_color_code=c.foreground.bright_blue(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    roof_room.insert_individual(
        char=v.char('~'),
        position=v.position(3, 3),
        property_=c.property(
            fg_color_code=c.foreground.red(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    roof_room.draw_horizontal_line(
        char=v.char('|'),
        position=v.position(2, 0),
        length=v.length(4),
        step=v.length(1),
        property_=c.property(
            fg_color_code=c.foreground.green(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    roof_room.draw_horizontal_line(
        char=v.char('|'),
        position=v.position(3, 0),
        length=v.length(2),
        step=v.length(5),
        property_=c.property(
            fg_color_code=c.foreground.green(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    # roof_room.draw()

    roof.insert_grid(
        position=v.position(3, 11),
        grid_=roof_room,
        remove_bg_mode=False
    )

    # roof.draw()

    ###############
    # Body
    ###############
    body: p.Grid = p.Grid(v.size(8, 29))

    body.draw_filled_box(
        char=v.char(':'),
        position=v.position(0, 0),
        size=v.size(8, 29),
        property_=c.property(
            fg_color_code=c.foreground.bright_yellow(),
            style_codes=[
                c.style.bold(),
                c.style.italic()
            ]
        )
    )

    ###############
    # Windows
    ###############
    window: p.Grid = p.Grid(v.size(3, 4))

    window.draw_filled_box(
        char=v.char('#'),
        position=v.position(0, 0),
        size=v.size(3, 4),
        property_=c.property(
            fg_color_code=c.foreground.bright_blue(),
            style_codes=[
                c.style.bold(),
                c.style.italic()
            ]
        )
    )

    window_large: p.Grid = p.Grid(v.size(3, 5))

    window_large.draw_filled_box(
        char=v.char('#'),
        position=v.position(0, 0),
        size=v.size(3, 5),
        property_=c.property(
            fg_color_code=c.foreground.bright_blue(),
            style_codes=[
                c.style.bold(),
                c.style.italic()
            ]
        )
    )

    # Inserting Windows
    window_positions: list[v.position] = [
        v.position(0, 5),
        v.position(4, 5),
        v.position(0, 20),
        v.position(4, 20),
    ]
    for position in window_positions:
        body.insert_grid(position=position, grid_=window)
    body.insert_grid(position=v.position(0, 12), grid_=window_large)

    ###############
    # Door
    ###############
    door: p.Grid = p.Grid(v.size(4, 5))

    for i in range(2):
        door.draw_vertical_line(
            char=v.char('I'),
            position=[v.position(0, 0), v.position(0, 4)][i],
            length=v.length(4),
            property_=c.property(
                fg_color_code=c.foreground.bright_magenta(),
                style_codes=[
                    c.style.dim()
                ]
            )
        )

        door.draw_horizontal_line(
            char=[v.char('~'), v.char('_')][i],
            position=[v.position(0, 1), v.position(3, 1)][i],
            length=v.length(3),
            property_=c.property(
                fg_color_code=c.foreground.magenta(),
                style_codes=[
                    c.style.dim()
                ]
            )
        )

    door.insert_individual(
        char=v.char(','),
        position=v.position(2, 1),
        property_=c.property(
            fg_color_code=c.foreground.bright_white(),
            style_codes=[
                c.style.bold()
            ]
        )
    )

    # door.draw()

    body.insert_grid(
        position=v.position(4, 12),
        grid_=door,
        remove_bg_mode=False
    )

    # body.draw()

    ##############################
    # Inserting parts
    ##############################
    house.insert_grid(v.position(0, 0), roof)       # Roof
    house.insert_grid(v.position(8, 0), body)       # Body


    house.draw()

    # Text
    text: p.Grid = p.Grid(v.size(1, 29))

    text.insert_text(
        position=v.position(0, 0),
        text=v.constant('Talha\'s House'),
        property_=c.property(
            fg_color_code=c.foreground.black(),
            bg_color_code=c.background.yellow()
        )
    )

    text.draw()
