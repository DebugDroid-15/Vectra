import re
from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression

class MatlabSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, is_dark: bool = False):
        super().__init__(parent)
        self.is_dark = is_dark
        self.highlighting_rules = []
        self._init_rules()

    def set_dark_mode(self, is_dark: bool):
        self.is_dark = is_dark
        self.highlighting_rules = []
        self._init_rules()
        self.rehighlight()

    def _init_rules(self):
        # Keywords format
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569cd6" if self.is_dark else "#0000FF"))
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            r"\bif\b", r"\belse\b", r"\belseif\b", r"\bend\b", r"\bfor\b",
            r"\bwhile\b", r"\bbreak\b", r"\bcontinue\b", r"\breturn\b",
            r"\bfunction\b", r"\bclc\b", r"\bclear\b"
        ]
        for kw in keywords:
            rule = (QRegularExpression(kw), keyword_format)
            self.highlighting_rules.append(rule)

        # Number format
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#b5cea8" if self.is_dark else "#0984e3"))
        rule = (QRegularExpression(r"\b[0-9]+(\.[0-9]+)?([eE][+-]?[0-9]+)?\b"), number_format)
        self.highlighting_rules.append(rule)

        # String format
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#ce9178" if self.is_dark else "#a29bfe"))
        rule = (QRegularExpression(r"'.*?'"), string_format)
        self.highlighting_rules.append(rule)

        # Comment format (%)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6a9955" if self.is_dark else "#008000"))
        comment_format.setFontItalic(True)
        rule = (QRegularExpression(r"%.*"), comment_format)
        self.highlighting_rules.append(rule)

    def highlightBlock(self, text: str):
        for pattern, fmt in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fmt)
