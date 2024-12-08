import argparse
from dz3 import ConfigParser

def main():
    parser = argparse.ArgumentParser(description='Convert XML to custom configuration language.')
    parser.add_argument('input_file', type=str, help='Path to the input XML file')
    parser.add_argument('output_file', type=str, help='Path to the output configuration file')

    args = parser.parse_args()

    config_parser = ConfigParser()
    config_parser.parse_file(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
