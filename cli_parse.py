from parse1 import main as parse1
from sys import argv as cli_args
from re import sub
# from parse2 import main as parse2

parser_func = parse1

url = 'https://www.tomshardware.com/reviews/cpu-hierarchy,4312.html'
xpath = '//*[@id="slice-container-V7teKs7ev9p3jsgMmVR9A-table-25"]/div[2]/table'
output_filename = 'web_table'

# Takes a filename, returns a safely-formatted filename
def sanitize_filename(filename):
    # Remove invalid characters
    filename = sub(r"[\/:*?'<>|]", '', filename)
    # Replace whitespace characters with an underscore
    filename = filename.replace(' ', '_')
    # Truncate the filename if it is too long
    max_length = 243
    if len(filename) > max_length:
        filename = filename[:max_length]
    return filename

def main(args):
    parser_func(*args)
if __name__ == '__main__':
    if len(cli_args) == 3:
        cli_args[1] = sanitize_filename(cli_args[1])
        main(cli_args[1:])
    else:
        main((url, output_filename, xpath))
