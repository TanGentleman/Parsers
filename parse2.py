from lxml import etree
from lxml import html as lhtml
import pandas as pd
import requests
import re

DIRECTORY = 'outputs/parse2'
EXAMPLE_URL = 'https://www.vgchartz.com/gamedb/'
EXAMPLE_XPATH = '//*[@id="generalBody"]/table[1]'
EXAMPLE_OUTPUT_FILE = 'example_table'
def url_to_html(url):
    """
    Fetches the HTML content of the given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.

    Raises:
        requests.HTTPError: If the request to fetch the URL fails.
    """
    response = requests.get(url)
    if response.status_code != 200:
        raise requests.HTTPError(f'Failed to fetch {url}.')
    if "text/html" not in response.headers["content-type"]:
        raise ValueError(f'URL {url} does not appear to contain HTML.')
    response.encoding = 'utf-8'
    return response.text

def extract_table(html, xpath = None):
    """
    Extracts the first HTML table found at the given XPath in the HTML content.

    Args:
        html (str): The HTML content.
        xpath (str): The XPath where the table is located.

    Returns:
        lxml.etree.Element: The HTML table.

    Raises:
        ValueError: If no table is found at the given XPath.
    """
    # Convert HTML string to lxml Element

    if xpath:
        tree = etree.HTML(html)
        tables = tree.xpath(xpath)
        # Check if table is not empty and contains at least one element
        if tables and len(tables) > 0:
            # Verify if the element(s) in table have the tag name "table"
            if all(elem.tag == "table" for elem in tables):
                print("Valid table(s) found!")
            else:
                print("Invalid table(s) found!")
        else:
            print("No table found!")
            raise ValueError(f"No table found at XPath: {xpath}")
        # How do I ensure that this is valid HTML for a table?
        return tables[0]
    else:
        tree = etree.HTML(html)
        # Find the first table
        table = tree.find('.//table')
        if table.tag == "table":
            print("Valid table found!")
            return table
        else:
            print("No table found!")
            raise ValueError(f"No table found! (XPATH==None)")

            
def remove_style_tags(html):
    # Remove style tags
    return re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)
        
def table_to_df(table):
    """
    Converts an HTML table to a pandas DataFrame.

    Args:
        table (lxml.etree.Element): The HTML table.

    Returns:
        pandas.DataFrame: The DataFrame.

    Raises:
        ValueError: If no table is found in the HTML.
    """
    # print(type(table), table, "<-- table \n")
    raw_html = etree.tostring(table, method='html').decode()
    # Remove the style tags from the HTML
    # raw_html = remove_style_tags(raw_html)
    dfs = pd.read_html(raw_html)
    
    if not dfs:
        raise ValueError("No table found in HTML")
    return dfs[0]

def main(input_string, output_file, xpath = None):
    """
    Scrapes a table from a webpage and saves it as a CSV file.

    Args:
        url (str): The URL to scrape.
        xpath (str): The XPath where the table is located.
        output_file (str): The output file name.
    """
    # try:
    #     html = url_to_html(url)
    #     table = extract_table(html, xpath)
    #     df = table_to_df(table)
    #     df.to_csv(f'{DIRECTORY}/{output_file}.csv', index=False)
    # except Exception as e:
    #     print(f"STEP 1 FAIL")
    #     return
    if input_string.startswith('http://') or input_string.startswith('https://'):
        # The input is a URL
        try:
            html = url_to_html(input_string)
        except:
            print('Invalid URL')
            return
    else:
        html = input_string
    try:
        table = extract_table(html, xpath)
        
    except Exception as e:
        print(f"Failed in html->data frame")
        print(e)
        return
    try:
        df = table_to_df(table)
        df.to_csv(f'{DIRECTORY}/{output_file}.csv', index=False)
    except:
        print("Failed to save csv file")

if __name__ == "__main__":
    """
    Scrapes a table from a webpage and saves it as a CSV file.

    Args:
        url (str): The URL to scrape.
        xpath (str): The XPath where the table is located.
        output_file (str): The output file name.
    """
    main(EXAMPLE_URL, EXAMPLE_OUTPUT_FILE, EXAMPLE_XPATH)
