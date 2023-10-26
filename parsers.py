""" 
    This is the flow for using the parsers library.
    Input is either a url, raw html, or a file, with an optional argument for XPATH string.
    You can choose the parsing algrithm (Parse1, Parse2) with the other being a Fallback.
    Output can be a list of tables, a table, or None.
    1. Make a class Parsnip
    2. Call the method parse() with the input and optional arguments
"""
from parse2 import url_to_html, remove_style_tags_regex
from pathlib import Path
import parse1
import parse2

def text_to_tree(text: str) -> any:
    # Implement logic to convert text to a tree
    pass

def validate_source(source: str) -> tuple[str, any] or None:
    if source == "":
        print('Empty source')
        return None
    text = ""
    if source.startswith('http'):
        # The input is a URL
        try:
            text = url_to_html(source)
        except Exception as e:
            # print(f"An error occurred: {e}")
            print('Invalid URL')
            return None
        if text is None:
            print('No table found')
            return None
    else:
        assert(source != "")
        if len(source) < 200 and Path(source).exists():
            # Input source is a file
            path = Path(source)
            text = path.read_text()
        else:
            text = source
    try:
        if text == "":
            print('Empty HTML. Text/tree not generated')
            return None
        tree = text_to_tree(text)
        return (text, tree)
    except:
        print('Invalid HTML. Tree not generated')
        return None
DEFAULT_PARSE_ALGO = "Parse1"
class Parsnip:
    def __init__(self, source, parse_algo = DEFAULT_PARSE_ALGO, XPATH = None, text = None, tree = None, soup = None, tables = None):
        if text is None:
            validation = validate_source(source)
            if validation is None:
                raise ValueError("Invalid source") 
            (self.text, self.tree) = validate_source(source)
            print("text and tree now set. (May not be valid HTML)")
            # Optional bs4 check using soup = BeautifulSoup(string, "html.parser")
        else:
            self.text = text
            self.tree = tree
        self.soup = None
        self.parse_algo = parse_algo
        self.XPATH = XPATH
        self.tables = tables
    
    def get_tables(self):
        # Implement logic to retrieve all tables from input_data using xpath and parsing_algorithm if provided
        tables = []
        if self.text:
            if self.parse_algo == "Parse1":
                if not self.soup:
                    self.soup = parse1.html_to_soup(self.text)
                    if not self.soup:
                        print("No soup. No tables.")
                        return None
                tables = parse1.find_tables(self.soup)
        else:
            print("No text to parse")
        self.tables = tables
        return str(tables)
        pass
    def rinse(self):
        # 
        if self.text:
            self.text = remove_style_tags_regex(self.text)
        else:
            "No text to rinse"
        # Implement logic to clean up the tables
        pass

    def get_first_table(self):
        # Implement logic to retrieve the first table from input_data using xpath and parsing_algorithm if provided
        if self.tables:
            return str(self.tables[0])
        else:
            pass
        pass

    def save_to_csv(self, table_data, file_path):
        # Implement logic to save table_data to a CSV file at the specified file_path
        pass
