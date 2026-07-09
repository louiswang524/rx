from rx_state.survey import PaperNote

PREAMBLE = r"""\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage{natbib}
"""


def render_bib(notes: list[PaperNote]) -> str:
    entries = []
    for n in notes:
        entries.append(
            f"@misc{{{n.key},\n"
            f"  title = {{{n.title}}},\n"
            f"  author = {{}},\n"
            f"  year = {{}},\n"
            f"}}"
        )
    return "\n\n".join(entries) + ("\n" if entries else "")
