from lxml import html as lhtml
from parse2 import url_to_html, extract_table, remove_style_tags_regex
from bs4 import BeautifulSoup
from bs4.element import Tag
import pandas as pd
from typing import List, Tuple

from time import time
import logging

DIRECTORY = 'outputs/parse1'
# EMPTY_COL_PLACEHOLDER = '*Col'
EMPTY_COL_PLACEHOLDER = None
SAVE_ALL_TABLES = False

import os

# Step 1: Get the path of the existing file
curr_file_path = os.path.abspath(__file__)

# Step 2: Extract the directory from the file path
parser_root_path = os.path.dirname(curr_file_path)

# Step 3: Set the root directory
OUTPUT_DIRECTORY = os.path.join(parser_root_path, DIRECTORY)

def save_string_to_file(content: str, filename: str) -> None:
    """
    Saves the given string content to a file.

    Args:
        content (str): The string content to be saved.
        filename (str): The name of the file to save the content to.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)

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
    table = extract_table(html, xpath)
    table_html = lhtml.tostring(table)
    return table_html
    
def remove_style_tags_bs4(soup: BeautifulSoup) -> BeautifulSoup:
    for style_tag in soup.find_all('style'):
        style_tag.decompose()
    return soup

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
    # table = soup.find('table')
    tables = soup.find_all('table')
    if tables:
        return tables[0]
    else:
        for child in soup.children:
            if child.name == 'table':
                return find_table(child)
        print("No table found")
        return None
        raise ValueError("No table found")

def extract_data(table: Tag) -> Tuple[List[str], List[List[str]]]:
    """OUTDATED
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
    thead = table.find('thead')
    if thead:
        # headers are gonna be used as column values
        headers = [(header.text.strip()) for header in thead.find_all('th')]
        data_rows = table.find('tbody').find_all('tr')
    else:
        headers = [header.text.strip() for header in all_rows[0].find_all(['th', 'td'])]
        data_rows = all_rows[1:]

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
    else:
        print("No data found")
        return
    # Check if headers were found
    if not headers:
        raise ValueError("No headers found")
    data = []
    for row in data_rows:
        cols = row.find_all(['th', 'td'])
        cols_data = []
        for col in cols:
            cols_data.append(col.text.strip())
        if len(headers) > max_cols:
            if EMPTY_COL_PLACEHOLDER is not None:
                cols_data += [EMPTY_COL_PLACEHOLDER + str(i) for i in range(max_cols+1, len(headers)+1)]
            else:
                cols_data += [''] * (len(headers) - max_cols)
        data.append(cols_data)
    if not data:
        raise ValueError("No data found")
    return headers, data

def main(input_string: str, output_filename: str, xpath: str=None) -> float:
    """
    Scrapes a table from a webpage or raw HTML and saves it as a CSV file.

    Args:
        input_string (str): The URL to scrape or the raw HTML.
        xpath (str): The XPath where the table is located.
        output_filename (str): The output file name.
    """
    success = False

    # Set up logging
    logging.basicConfig(filename='logfile.log', level=logging.INFO)

    # Start the timer
    start_time = time()



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
        if html is None:
            print('No table found')
            return
    else:
        # The input is raw HTML
        html = input_string
    try:
        soup = BeautifulSoup(html, 'html.parser')
        soup = remove_style_tags_bs4(soup)
        print('soup obtained')
    except:
        print('Invalid HTML')
        return
    try:
        table = find_table(soup)
    except:
        print('No table found')
        return
    ### NEW
    try:
        table_html = table.prettify()
        if False:
            polished_html = remove_style_tags_regex(table_html)
        else:
            polished_html = table_html
        #REMEMBER TO INCLUDE POLISHED IN LINE BELOW
        dfs = pd.read_html(polished_html)
        if not dfs:
            raise ValueError("No table found in HTML")
        # save all the tables to csv
        if (len(dfs) > 1) and (SAVE_ALL_TABLES):
            # make a folder called output_filename
            # save each table to a csv file in that folder
            folder_path = f'{OUTPUT_DIRECTORY}/{output_filename}'
            os.mkdir(folder_path)
            for i, df in enumerate(dfs):
                df.to_csv(f'{folder_path}/{output_filename}_{i}.csv', index=False)
        else:
            df = dfs[0]
            df.to_csv(f'{OUTPUT_DIRECTORY}/{output_filename}.csv', index=False)
        success = True
    except Exception as e:
        print(f"An error occurred: {e}")
        # End the timer
    end_time = time()
    execution_time = end_time - start_time
    logging.info(f"{'P1 Success!' if success else 'Empty.'} Execution time: {execution_time} seconds")
    return execution_time


    ###LEGACY (This would need a solid implementation for extract_data)
    # legacy = False
    # if legacy:
    #     try:
    #         headers, data = extract_data(table)
    #     except Exception as e:
    #         print('Data not extracted: ', e)
    #         return
    #     try:
    #         df = pd.DataFrame(data, columns=headers)
    #         df.to_csv(f'{output_filename}.csv', index=False)
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #     return