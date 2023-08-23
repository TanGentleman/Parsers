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
from tests import ACTIVE_SET, DEFAULT_PARSER, RUN_BOTH_PARALLEL
# SET1 = tests.test1()
# SET2 = tests.test2()
# SET3 = tests.test3()
if DEFAULT_PARSER == "parse1":
    parser_func = parse1
elif DEFAULT_PARSER == "parse2":
    parser_func = parse2
else:
    raise ValueError("PARSER must be either 'parse1' or 'parse2'")

def run_tests(parser_func) -> list:
    exec_times = []
    for test in ACTIVE_SET:
        attempt_time = parser_func(*test())
        exec_times.append(attempt_time)
    return exec_times
    # parser_func(*SET1)
    # parser_func(*SET2)
    # parser_func(*SET3) 
    # parser_func(url, output_filename, xpath)
    # parser_func(html, output_filename)

import concurrent.futures
import logging
logging.basicConfig(filename='logfile.log', level=logging.INFO)
def function1():
    return run_tests(parse1)

def function2():
    return run_tests(parse2)

def run_parallel():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit function1 to the executor
        future1 = executor.submit(function1)
        
        # Submit function2 to the executor
        future2 = executor.submit(function2)

        # Wait for both functions to complete
        concurrent.futures.wait([future1, future2], return_when=concurrent.futures.FIRST_COMPLETED)
        parse1_total_time = sum(future1.result())
        parse2_total_time = sum(future2.result())

        if future1.done() and future2.done():
            if parse1_total_time < parse2_total_time:
                faster_function = "Parse1"
                percentage = (parse2_total_time - parse1_total_time) / parse2_total_time * 100
            else:
                faster_function = "Parse2"
                percentage = round((parse1_total_time - parse2_total_time) / parse1_total_time * 100, 2)

            logging.info(f"{faster_function} completed faster by {percentage}%")
        # Check which function completed first
if RUN_BOTH_PARALLEL == False:
    run_tests(parser_func)
else:
    run_parallel()