from base_markup import Markup
from rst_markup import RstMarkup
from markdown_markup import MarkdownMarkup

def markup_by_filename(filename):
    if filename.lower().endswith('.rst'):
        return RstMarkup()
    if filename.lower().endswith('.md'):
        return MarkdownMarkup()
    else:
        return Markup()