import PyMisc.color as clr

ui: dict = {
    'menu' : {
        'main' : {
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
            ),

            # Heading text
            'heading-text' : 'Main Menu',
        }
    }
}