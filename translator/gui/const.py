from dataclasses import dataclass


@dataclass
class LangItem:
    name: str
    code: str


LANG = [
    LangItem('Auto-detect', 'auto'),
    LangItem('English', 'en'),
    LangItem('Korean', 'ko'),
    LangItem('Indonesia', 'id'),
    LangItem('Vietnamese', 'vi'),
    LangItem('Chinese', 'zh'),
    LangItem('Japanese', 'ja'),
    LangItem('French', 'fr'),
]
