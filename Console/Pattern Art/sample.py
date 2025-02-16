import PyMisc.variable as var
import PyMisc.pattern as pattern
import PyMisc.color as color

if __name__ == '__main__':
    # Pattern - Grid
    grid: pattern.Grid = pattern.Grid(var.size(8, 8))

    # Filled Box
    grid.draw_filled_box(
        var.char('-'),                                  # Character
        var.position(2, 2),                 # Position
        var.size(4, 4),                    # Size

        # Color Property
        color.property(
            color.foreground.bright_yellow()            # Foreground color
        )
    )

    # Hollow Box 1
    grid.draw_hollow_box(
        var.char('*'),                                  # Character
        var.position(0, 0),                 # Position
        var.size(8, 8),                    # Size

        # Color Property
        color.property(
            color.foreground.red()                      # Foreground color
        )
    )

    # Hollow Box 2
    grid.draw_hollow_box(
        var.char('+'),                                  # Character
        var.position(1, 1),                 # Position
        var.size(6, 6),                    # Size

        # Color Property
        color.property(
            color.foreground.bright_black(),            # Foreground color
            color.background.white()                    # Background Color
        )
    )

    # Corner Points
    grid.insert_individual(
        var.char('O'),                                  # Character
        var.position(0, 0),                 # Position

        # Color Property
        color.property(
            color.foreground.bright_yellow(),           # Foreground color
        )
    )

    grid.insert_individual(
        var.char('O'),                                  # Character
        var.position(0, 7),                 # Position

        # Color Property
        color.property(
            color.foreground.bright_yellow(),           # Foreground color
        )
    )

    grid.insert_individual(
        var.char('O'),                                  # Character
        var.position(7, 0),                 # Position

        # Color Property
        color.property(
            color.foreground.bright_yellow(),           # Foreground color
        )
    )

    grid.insert_individual(
        var.char('O'),                                  # Character
        var.position(7, 7),                 # Position

        # Color Property
        color.property(
            color.foreground.bright_yellow(),           # Foreground color
        )
    )

    # Line
    grid.draw_horizontal_line(
        var.char('^'),                                  # Character
        var.position(1, 1),                 # Position
        var.length(3),                                  # Length of the line
        var.length(2),                                  # Length of the gap between

        # Color Property
        color.property(
            color.foreground.bright_blue(),             # Foreground
            color.background.red(),                     # Background

            # Style
            [
                color.style.bold()                      # Bold
            ]
        )
    )

    # Create a new grid
    new_grid: pattern.Grid = pattern.Grid(var.size(2, 2))

    # Create a filled box in new grid
    new_grid.draw_filled_box(
        var.char('%'),                                  # Character
        var.position(0, 0),                 # Position
        var.size(2, 2),                    # Size

        # Color Property
        color.property(
            color.foreground.green()                    # Foreground
        )
    )

    # Insert the new grid
    grid.insert_grid(var.position(2, 2), new_grid)   # 1
    grid.insert_grid(var.position(3, 3), new_grid)   # 2
    grid.insert_grid(var.position(4, 4), new_grid)   # 3

    # Print the pattern
    grid.draw()
