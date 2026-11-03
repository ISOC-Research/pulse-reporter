"""
isoc_theme.py
=============
Single source of truth for the ISOC brand palette / fonts extracted from
ISOC_Sample.docx (word/theme/theme1.xml and table fills). Used by the Word
builder and by the HTML templates so both outputs share one look.
"""

DARK_NAVY = "0C1C2C"      # body text (dk1)
NAVY_TABLE = "0F2A47"     # table header fill
BRIGHT_BLUE = "3A82E4"    # Heading 1 / accent2
DEEP_INDIGO = "24366E"    # Heading 2 / accent1
H3_NAVY = "121A36"
H4_NAVY = "1B2852"
TEAL = "40B2A4"
PLUM = "7E245C"
CORAL = "D25238"
GOLD = "EECA4A"
OFF_WHITE = "EEF2EC"
WARM_GREY = "DEDAD0"

BODY_TEXT = DARK_NAVY
TABLE_FONT = "Arial"

CHART_PALETTE = [BRIGHT_BLUE, DEEP_INDIGO, TEAL, CORAL, GOLD, PLUM, "7FA9E8", "8C9BC4"]
