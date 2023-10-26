###
input1 = 'https://www.vgchartz.com/gamedb/'
xpath1 = '//*[@id="generalBody"]/table[1]'
output_file1 = 'table1'
###
input2 = 'https://en.wikipedia.org/wiki/Wikipedia:Record_charts/Billboard_charts_guide'
xpath2 = '//*[@id="mw-content-text"]/div[1]/div[4]/table'
output_file2 = 'table2'
###
input3 = 'https://en.wikipedia.org/wiki/List_of_particles'
xpath3 = '//*[@id="mw-content-text"]/div[1]/dl/dd/table'
output_file3 = 'table3'
###
input4 = 'https://en.wikipedia.org/wiki/Graviton'
xpath4 = '//*[@id="mw-content-text"]/div[1]/div[7]/table'
output_file4 = 'table4'
### This one breaks!
input5 = 'https://openstax.org/books/college-physics/pages/1-2-physical-quantities-and-units'
xpath5 = '//*[@id="import-auto-id1677589"]/table'
output_file5 = 'table5'
###
input6 = 'https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html'
xpath6 = '//*[@id="plotting-with-missing-data"]/table'
output_file6 = 'table6'
###
input7 = 'https://en.wikipedia.org/wiki/Composite_material'
xpath7 = '//*[@id="mw-content-text"]/div[1]/table[2]'
output_file7 = 'table7'
###
input8 = 'https://en.wikipedia.org/wiki/List_of_particles'
xpath8 = '//*[@id="mw-content-text"]/div[1]/div[16]/table'
output_file8 = 'table8'
###
input9 = 'https://en.wikipedia.org/wiki/Sun'
xpath9 = '//*[@id="mw-content-text"]/div[1]/div[33]/table'
output_file9 = 'table9'
###

###
input13 = 'https://birdsoftheworld.org/bow/home'
xpath13 = '//*[@id="content"]/div[6]/div/div/div[2]/table'
output_file13 = 'table13'
# Test cases
def test1():
    return (input1, output_file1, xpath1)
def test2():
    return (input2, output_file2, xpath2)
def test3():
    return (input3, output_file3, xpath3)
def test4():
    return (input4, output_file4, xpath4)
def test5():
    return (input5, output_file5, xpath5)
def test6():
    return (input6, output_file6, xpath6)
def test7():
    return (input7, output_file7, xpath7)
def test8():
    return (input8, output_file8, xpath8)
def test9():
    return (input9, output_file9, xpath9)
def test10():
    with open('html_strings/random.html', 'r') as f:
        html = f.read()
    input10 = html
    xpath10 = None
    output_file10 = 'table10'
    return (input10, output_file10, xpath10)
def test11():
    with open('html_strings/wechess_table.html', 'r') as f:
        html = f.read()
    input11 = html
    xpath11 = None
    output_file11 = 'table11'
    return (input11, output_file11, xpath11)
def test12():
    with open('html_strings/nasty,html', 'r') as f:
        html = f.read()
    input12 = html
    xpath12 = None
    output_file12 = 'table12'
    return (input12, output_file12, xpath12)
def test13():
    return (input13, output_file13, xpath13)
def test14():
    with open('html_strings/complex_table.html', 'r') as f:
        html = f.read()
    input14 = html
    xpath14 = None
    output_file14 = 'table14'
    return (input14, output_file14, xpath14)
def test15():
    with open('html_strings/complex_table2.html', 'r') as f:
        html = f.read()
    input15 = html
    xpath15 = None
    output_file15 = 'table15'
    return (input15, output_file15, xpath15)
def test16():
    input16 = 'https://en.wikipedia.org/wiki/Wikipedia:Random'
    xpath16 = None
    output_file16 = 'table16'
    return (input16, output_file16, xpath16)
def test17():
    input17 = '<table class="market_commodity_orders_table"><tbody><tr><th align="right">Price</th><th align="right">Quantity</th></tr><tr><td align="right" class="">$24.30</td><td align="right">7</td></tr><tr><td align="right" class="">$24.32</td><td align="right">1</td></tr><tr><td align="right" class="">$25.39</td><td align="right">1</td></tr><tr><td align="right" class="">$26.01</td><td align="right">25</td></tr><tr><td align="right" class="">$26.02</td><td align="right">2</td></tr><tr><td align="right" class="">$26.22 or more</td><td align="right">44</td></tr></tbody></table>'
    # xpath17 = '//*[@id="mw-content-text"]/div[1]/div[16]/table'
    xpath17 = None
    output_file17 = 'table17'
    return (input17, output_file17, xpath17)
ACTIVE_SET = [test17]
DEFAULT_PARSER = "parse1"
RUN_BOTH_PARALLEL = True
