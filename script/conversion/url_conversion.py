#!/usr/bin/env python3
import re


def update_markdown_urls(content: str) -> str:
    base_url = "https://minbzk.github.io/Algoritmekader"

    patterns = [
        (
            r"\[(.*?)\]\(../maatregelen/(.*?)\.md\)",
            rf"[\1]({base_url}/voldoen-aan-wetten-en-regels/maatregelen/\2/index.html)",
        ),
        (r"\[(.*?)\]\(([0-9]-.*?)\.md\)", rf"[\1]({base_url}/voldoen-aan-wetten-en-regels/maatregelen/\2/index.html)"),
        (
            r"\[(.*?)\]\(../vereisten/(.*?)\.md\)",
            rf"[\1]({base_url}/voldoen-aan-wetten-en-regels/vereisten/\2/index.html)",
        ),
        (r"\[(.*?)\]\(../../levenscyclus/(.*?)\.md\)", rf"[\1]({base_url}/levenscyclus/\2/)"),
    ]

    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)

    return content
