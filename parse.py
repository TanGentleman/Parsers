from parse1 import main as parse1
from parse2 import main as parse2

url = 'https://en.wikipedia.org/wiki/Wikipedia:Record_charts/Billboard_charts_guide'
xpath = '//*[@id="mw-content-text"]/div[1]/div[4]/table'
output_filename = 'web_table'
# html = r""""""


# parse1(html, output_filename)
# parse1(url, output_filename, xpath)
# parse2(url, output_filename, xpath)

### Test cases
import tests
SET1 = tests.test1()
SET2 = tests.test2()
SET3 = tests.test3()

parser_func = parse1
# parser_func = parse2

def run_tests(parser_func):
    parser_func(*SET1)
    parser_func(*SET2)
    parser_func(*SET3)

run_tests(parser_func)