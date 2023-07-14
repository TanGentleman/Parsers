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

# Test cases
def test1():
    return (input1, output_file1, xpath1)
def test2():
    return (input2, output_file2, xpath2)
def test3():
    return (input3, output_file3, xpath3)
