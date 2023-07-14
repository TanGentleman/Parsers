import pandas as pd
from lxml import html as lhtml
from parse2 import url_to_html
def main(input_string: str, output_filename, xpath: str=None):
    from bs4 import BeautifulSoup
    
    def get_table_from_xpath(html: str, xpath: str):
        tree = lhtml.fromstring(html)
        elements = tree.xpath(xpath)
        if elements:
            table_element = elements[0]
            table_html = lhtml.tostring(table_element).decode()
            return table_html
        else:
            return None
    if input_string.startswith('http://') or input_string.startswith('https://'):
        # The input is a URL
        html = url_to_html(input_string)
        if xpath is not None:
            html = get_table_from_xpath(html, xpath)
    else:
        # The input is raw HTML
        html = input_string
    
    # Your code to convert table to CSV goes here.
    soup = BeautifulSoup(html, 'html.parser')
    

    def find_table(soup):
        table = soup.find('table')
        if table:
            return table
        else:
            for child in soup.children:
                if child.name == 'table':
                    return find_table(child)
            return None

    table = find_table(soup)
    if not table:
        raise ValueError("No table found")

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


    # # We only extract the headers within the 'thead' tag
    # if table.find('thead'):
    #     headers = [header.text.strip() for header in table.find('thead').find_all('th')]
    #     rows = table.find('tbody').find_all('tr')
    # else:
    #     headers = [header.text.strip() for header in table.find('tbody').find_all('tr')[0].find_all('th')]
    #     # remove the first row since it's the header
    #     rows = table.find('tbody').find_all('tr')[1:]

    # Check if headers were found
    if not headers:
        raise ValueError("No headers found")

    # If headers are less than the columns in data_rows, fill the headers with default values
    if data_rows:
        # Find the maximum number of columns in any row
        max_cols = max(len(row.find_all(['th', 'td'])) for row in data_rows)
        # If headers are less than the max_cols, fill the headers with default values
        if len(headers) < max_cols:
            headers += ['*Col_'+str(i) for i in range(len(headers)+1, max_cols+1)]

    data = []
    for row in data_rows:
        cols = row.find_all(['th', 'td'])
        # Replace newlines and multiple spaces in the column text
        cols_data = []
        for col in cols:
            # INACTIVE CLAUSE to add href links
            if False and col.find('a'):  # if an anchor tag is found
                # base_url = "https://example.com"  # Specify the base URL here
                href = col.find('a').get('href')
                if href.startswith('/'):  # if the href starts with a forward slash
                    href = base_url + href  # prepend the base URL
                cols_data.append(col.text.strip() + " (" + href + ")")
            else:  # if no anchor tag is found
                cols_data.append(col.text.strip())
        data.append(cols_data)

    # print(data)
    # Check if data was found
    if not data:
        raise ValueError("No data found")

    try:
        df = pd.DataFrame(data, columns=headers)
        df.to_csv(f'{output_filename}.csv', index=False)
    except Exception as e:
        print(f"An error occurred: {e}")
    return None
