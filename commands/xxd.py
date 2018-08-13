""" darkbox template for a command """

import argparse
import binascii

def sidebar_str(s):
    return ''.join(chr(i) if 0x19<i<0x7f else '.' for i in s)


class xxd:
    def __init__(self):
        self.version = '0.0.1'

    def get_parser(self):
        parser = argparse.ArgumentParser(description="produce or reverse hexdumps")
        parser.add_argument("-r", "--reverse", action="store_true")
        parser.add_argument("-u", "--uppercase", action="store_true")
        parser.add_argument("-p", "--plain", action="store_true")
        parser.add_argument("-c", "--cols", type=int, default=16)
        parser.add_argument('-v', '--version', default=False, action='store_true')
        parser.add_argument("file", nargs='?')
        return parser
    
    def run(self):
        parser = self.get_parser()
        args = vars(parser.parse_args())
        if args['version']:
            print('darkbox {} v{}'.format(self.__class__.__name__, self.version))
            return
        
        with open(args['file'], 'rb') as f:
            line_counter = 0
            while True:
                raw_line = f.read(args['cols'])
                if not raw_line: break # line is empty; EOF
                hex_line = binascii.hexlify(raw_line).decode("utf-8")

                if args['uppercase']:
                    hex_line = hex_line.upper()

                if args['plain']:
                    print(hex_line, end='')
                
                else:
                    hex_line = ' '.join(hex_line[i:i+4] for i in range(0, len(hex_line), 4))
                    hex_counter = hex(line_counter * args['cols'])[2:].zfill(8)
                    print("{}: {}  {}".format(hex_counter, hex_line, sidebar_str(raw_line)))

                line_counter += 1

        print('')