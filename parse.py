from parse1 import main as parse1
from parse2 import main as parse2

url = 'https://en.wikipedia.org/wiki/C%2B%2B'
xpath = '//*[@id="mw-content-text"]/div[1]/table[2]'
output_filename = 'example'
html = r"""
<table>
    <thead>
        <tr>
            <th>Header 1</th>
            <th>Header 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Data 1</td>
            <td>Data 2</td>
        </tr>
    </tbody>
</table>
"""
# parse1(html, output_filename)
# parse1(url, output_filename, xpath)
# parse2(url, output_filename, xpath)

### Test cases
import tests
from tests import ACTIVE_SET, DEFAULT_PARSER
# SET1 = tests.test1()
# SET2 = tests.test2()
# SET3 = tests.test3()
if DEFAULT_PARSER == "parse1":
    parser_func = parse1
elif DEFAULT_PARSER == "parse2":
    parser_func = parse2
else:
    raise ValueError("PARSER must be either 'parse1' or 'parse2'")

def run_tests(parser_func):
    for test in ACTIVE_SET:
        parser_func(*test())
    # parser_func(*SET1)
    # parser_func(*SET2)
    # parser_func(*SET3) 
    # parser_func(url, output_filename, xpath)
    # parser_func(html, output_filename)

run_tests(parser_func)
