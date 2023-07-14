from lxml import etree
import pandas as pd
import requests
import re
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
        raise requests.HTTPError(f'Failed to fetch {url}. Server responded with status {response.status_code}.')
    if "text/html" not in response.headers["content-type"]:
        raise ValueError(f'URL {url} does not appear to contain HTML.')
    return response.text

def extract_table(html, xpath):
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
    tree = etree.HTML(html)
    tables = tree.xpath(xpath)
    if not tables:
        raise ValueError(f"No table found at XPath: {xpath}")
    return tables[0]

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
    raw_html = etree.tostring(table, method='html').decode()
    # Remove the style tags from the HTML
    raw_html = re.sub(r'<style.*?>.*?</style>', '', raw_html, flags=re.DOTALL)
    dfs = pd.read_html(raw_html)
    if not dfs:
        raise ValueError("No table found in HTML")
    return dfs[0]

def main(url, output_file, xpath, ):
    """
    Scrapes a table from a webpage and saves it as a CSV file.

    Args:
        url (str): The URL to scrape.
        xpath (str): The XPath where the table is located.
        output_file (str): The output file name.
    """
    html = url_to_html(url)
    table = extract_table(html, xpath)
    df = table_to_df(table)
    df.to_csv(f'{output_file}.csv', index=False)

if __name__ == "__main__":
    """
    Scrapes a table from a webpage and saves it as a CSV file.

    Args:
        url (str): The URL to scrape.
        xpath (str): The XPath where the table is located.
        output_file (str): The output file name.
    """
    url = 'https://www.vgchartz.com/gamedb/'
    xpath = '//*[@id="generalBody"]/table[1]'
    output_file = 'lxml_table.csv'
    main(url, output_file, xpath)
