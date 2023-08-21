from parse1 import main as parse1
from sys import argv as cli_args
from re import sub
# from parse2 import main as parse2

parser_func = parse1

url = 'https://en.wikipedia.org/wiki/C%2B%2B'
xpath = '//*[@id="mw-content-text"]/div[1]/table[2]'
output_filename = 'example_cli_parse'

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
    cli_len = len(cli_args)
    if (cli_len in [3,4]):
        cli_args[2] = sanitize_filename(cli_args[2])
        main(cli_args[1:])
    elif len(cli_args) == 1:
        print("Default cli_args used")
        main((url, output_filename, xpath))
    else:
        print("Bad CLI Arguments")
