class Styles:
    PRIMARY_GREEN = "#2e7d32"
    SECONDARY_GREEN = "#4caf50"
    LIGHT_GREEN = "#c8e6c9"
    EARTH_BROWN = "#795548"
    LIGHT_BROWN = "#bcaaa4"
    CREAM = "#fafafa"
    WHITE = "#ffffff"
    DARK_TEXT = "#263238"

    MAIN_STYLE = f"""
        QMainWindow {{
            background-color: {CREAM};
        }}
        QWidget {{
            background-color: {CREAM};
            color: {DARK_TEXT};
        }}
    """

    # Button styles
    PRIMARY_BUTTON = f"""
        QPushButton {{
            background-color: {PRIMARY_GREEN};
            color: white;
            font-weight: bold;
            font-size: 14px;
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            min-height: 20px;
        }}
        QPushButton:hover {{
            background-color: {SECONDARY_GREEN};
        }}
        QPushButton:pressed {{
            background-color: #1b5e20;
        }}
    """

    SECONDARY_BUTTON = f"""
        QPushButton {{
            background-color: {SECONDARY_GREEN};
            color: white;
            font-weight: bold;
            font-size: 14px;
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            min-height: 20px;
        }}
        QPushButton:hover {{
            background-color: {PRIMARY_GREEN};
        }}
    """

    # Card style
    CARD_STYLE = f"""
        QFrame {{
            background-color: {WHITE};
            border: 1px solid {LIGHT_GREEN};
            border-radius: 8px;
            padding: 15px;
            margin: 5px;
        }}
    """

    # Input field style
    INPUT_STYLE = f"""
        QLineEdit, QTextEdit {{
            padding: 12px;
            border: 2px solid {LIGHT_BROWN};
            border-radius: 8px;
            font-size: 14px;
            background-color: {WHITE};
            color: {DARK_TEXT};
        }}
        QLineEdit:focus, QTextEdit:focus {{
            border-color: {PRIMARY_GREEN};
            background-color: {LIGHT_GREEN};
        }}
    """

    # Action button styles
    ACTION_BUTTON = """
        QPushButton {
            background-color: #4caf50;
            color: white;
            font-weight: bold;
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            font-size: 12px;
            min-width: 80px;
            min-height: 35px;
        }
        QPushButton:hover {
            background-color: #2e7d32;
        }
    """

    DELETE_BUTTON = """
        QPushButton {
            background-color: #dc3545;
            color: white;
            font-weight: bold;
            padding: 8px 12px;
            border: none;
            border-radius: 5px;
            font-size: 12px;
            min-width: 80px;
            min-height: 35px;
        }
        QPushButton:hover {
            background-color: #c82333;
        }
    """
