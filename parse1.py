from lxml import html as lhtml
from parse2 import url_to_html
from bs4 import BeautifulSoup
from bs4.element import Tag
import pandas as pd
from typing import List, Tuple

EMPTY_COL_PLACEHOLDER = '*Col'
EMPTY_COL_PLACEHOLDER = None

def get_table_from_xpath(html: str, xpath: str) -> str:
    """
    Extracts the first HTML table found at the given XPath in the HTML content.

    Args:
        html (str): The HTML content.
        xpath (str): The XPath where the table is located.

    Returns:
        str: The HTML table.

    Raises:
        ValueError: If no table is found at the given XPath.
    """
    tree = lhtml.fromstring(html)
    elements = tree.xpath(xpath)
    if elements:
        table_element = elements[0]
        table_html = lhtml.tostring(table_element).decode()
        return table_html
    else:
        return None

def find_table(soup: BeautifulSoup) -> Tag:
    """
    Finds the first table in the BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object.

    Returns:
        bs4.element.Tag: The table.

    Raises:
        ValueError: If no table is found.
    """
    table = soup.find('table')
    if table:
        return table
    else:
        for child in soup.children:
            if child.name == 'table':
                return find_table(child)
        raise ValueError("No table found")

def extract_data(table: Tag) -> Tuple[List[str], List[List[str]]]:
    """
    Extracts the data from the table.

    Args:
        table (bs4.element.Tag): The table.

    Returns:
        Tuple[List[str], List[List[str]]]: The headers and data.

    Raises:
        ValueError: If no data is found.
    """
    # Extract all rows
    all_rows = table.find_all(['tr'])
    # Check if rows were found
    if not all_rows:
        raise ValueError("No rows found")
    # Extract headers
    if table.find('thead'):
        # headers are gonna be used as column values
        headers = [header.text.strip() for header in table.find('thead').find_all('th')]
        data_rows = table.find('tbody').find_all('tr')
    else:
        headers = [header.text.strip() for header in all_rows[0].find_all(['th', 'td'])]
        data_rows = all_rows[1:]

    # Check if headers were found
    if not headers:
        raise ValueError("No headers found")

    # If headers are less than the columns in data_rows, fill the headers with default values
    if data_rows:
        # Find the maximum number of columns in any row
        max_cols = max(len(row.find_all(['th', 'td'])) for row in data_rows)
        # If headers are less than the max_cols, fill the headers with default values
        if len(headers) < max_cols:
            if EMPTY_COL_PLACEHOLDER is not None:
                headers += [EMPTY_COL_PLACEHOLDER + str(i) for i in range(len(headers)+1, max_cols+1)]
            else:
                headers += [''] * (max_cols - len(headers))

    data = []
    for row in data_rows:
        cols = row.find_all(['th', 'td'])
        # Replace newlines and multiple spaces in the column text
        cols_data = []
        for col in cols:
            cols_data.append(col.text.strip())
        data.append(cols_data)

    return headers, data

def main(input_string: str, output_filename: str, xpath: str=None) -> None:
    """
    Scrapes a table from a webpage or raw HTML and saves it as a CSV file.

    Args:
        input_string (str): The URL to scrape or the raw HTML.
        xpath (str): The XPath where the table is located.
        output_filename (str): The output file name.
    """
    if input_string.startswith('http://') or input_string.startswith('https://'):
        # The input is a URL
        try:
            html = url_to_html(input_string)
        except Exception as e:
            # print(f"An error occurred: {e}")
            print('Invalid URL')
            return
        if xpath is not None:
            try:
                html = get_table_from_xpath(html, xpath)
            except:
                print('Invalid XPath')
                return
    else:
        # The input is raw HTML
        html = input_string
    
    soup = BeautifulSoup(html, 'html.parser')
    table = find_table(soup)
    headers, data = extract_data(table)

    if not data:
        raise ValueError("No data found")

    try:
        df = pd.DataFrame(data, columns=headers)
        df.to_csv(f'{output_filename}.csv', index=False)
    except Exception as e:
        print(f"An error occurred: {e}")
