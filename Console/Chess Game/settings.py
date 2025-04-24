import PyMisc.color as clr
from unicode import *

ui: dict = {
    'text' : {
        'default' : {
            'heading-symbol' : '*',
            'heading-color' : clr.property(
                clr.foreground.white()
            ),

            'text-content' : 'Sample Text',
            'text-color' : clr.property(
                clr.foreground.magenta(),
                None,
                clr.style.bold()
            )
        },
    },

    'menu' : {
        # Decorator of the Main Menu
        'decorator-symbol' : '#',
        'decorator-color' : clr.property(
            clr.property(
                clr.foreground.bright_blue(),
                clr.background.black(),
                [
                    clr.style.bold(),
                    clr.style.italic()
                ]
            )
        )
    }
}

board: dict = {
    # Empty cell
    'empty-black-symbol' : SYMBOL['empty-black'],
    'empty-black-color' : clr.property(
        clr.foreground.red(),
        None,
        clr.style.bold()
    ),

    'empty-white-symbol' : SYMBOL['empty-white'],
    'empty-white-color' : clr.property(
        clr.foreground.blue(),
        None,
        clr.style.bold()
    ),

    # Seperator
    'column-separator-symbol' : '|',
    'column-separator-color' : clr.property(
        clr.foreground.bright_white(),
        None,
        clr.style.bold()
    ),

    'row-separator-symbol' : '---------------------------------',
    'row-separator-color' : clr.property(
        clr.foreground.bright_white(),
        None,
        clr.style.bold()
    ),

    # Numbers
    'number-color' : clr.property(
        clr.foreground.black(),
        clr.background.white(),
        clr.style.bold()
    )
}