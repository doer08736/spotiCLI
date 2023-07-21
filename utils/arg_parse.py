from sys import stdout
from shutil import get_terminal_size
from optparse import OptionParser, IndentedHelpFormatter


class spotiCLIHelpFormatter(IndentedHelpFormatter):
    def __init__(self):
        max_width = get_terminal_size().columns or 80
        super().__init__(
            width=max_width, 
            max_help_position=int(.65 * max_width)
        )
    
class spotiCLIOptionParser(OptionParser):
    def __init__(self):
        super().__init__(
            usage="%prog -h | -p | -v | -d | -i | -s\nUsage: %prog -c <playlistname> | -t <trackname> | -a <artistname>",
            epilog="FOLLOW ME RN: [https://github.com/doer08736]",
            formatter=spotiCLIHelpFormatter()
        )
    
    def print_help(self, file=None):
        print("""
                      _   _  _____ _      _____ 
                     | | (_)/ ____| |    |_   _|
      ___ _ __   ___ | |_ _| |    | |      | |  
     / __| '_ \ / _ \| __| | |    | |      | |  
     \__ \ |_) | (_) | |_| | |____| |____ _| |_ 
     |___/ .__/ \___/ \__|_|\_____|______|_____|
         | |                                        v1.0
         |_|
        
        [https://github.com/doer08736/spotiCLI]                                    
        """)
        if file is None:
            file = stdout
        file.write(self.format_help())


parser = spotiCLIOptionParser()
parser.add_option("-p", "--playing", action="store_true", help="display current playing track")
parser.add_option("-v", "--viewplaylist", action="store_true", help="display user playlist(s)")
parser.add_option("-c", "--createplaylist", action="store_true", help="create playlist(s)")
parser.add_option("-d", "--deleteplaylist", action="store_true", help="delete playlist(s)")
parser.add_option("-t", "--trackinfo", action="store_true", help="display given track info")
parser.add_option("-a", "--artistinfo", action="store_true", help="display given artist info")
parser.add_option("-i", "--insert", action="store_true", help="insert track into playlist at specific position")
parser.add_option("-s", "--sort", action="store_true", help="sort playlist(s) according to release date")

options, args = parser.parse_args()