
import os
import datetime
from shutil import copytree, copy
from pathlib import Path


def calc_dir_size(dir):
    dirSize = 0

    for root, dirs, files in os.walk(dir, topdown=True):
        for name in files:
            dirSize += os.path.getsize(os.path.join(root, name))

    return dirSize


def readable_size(numBytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    index = 0

    while numBytes >= 1024 and index < len(suffixes) - 1:
        numBytes /= 1024
        index += 1

    # Convert bytes to a double digit decimal number
    decimal = ('%.2f' % numBytes).rstrip('0').rstrip('.')

    return '%s %s' % (decimal, suffixes[index])


if __name__ == '__main__':

    inputFile = input('Input file: ')
    outputDir = input('Output directory: ')

    output = outputDir + '/System_Backup_' + datetime.date.today().strftime('%m-%d-%Y')

    dest = Path(output)

    with open(inputFile, 'r') as f:
        lines = f.read().splitlines()

        numBytes = 0

        # Validate input file and calculate total backup size
        for line in lines:
            if os.path.isfile(line):
                numBytes += os.path.getsize(line)
            elif os.path.isdir(line):
                numBytes += calc_dir_size(line)
            else:
                raise ValueError('Invalid file or directory in input file: ' + line)

        print()
        print('Total size of backup: ' + readable_size(numBytes))
        print('Working...')

        # Copy each backup item to the destination directory
        for line in lines:
            try:
                if os.path.isfile(line):
                    copy(line, str(dest.absolute()))
                elif os.path.isdir(line):
                    # Create new version of input file directory in the backup directory
                    copiedDirectory = Path(str(dest.absolute()) + '/' + os.path.basename(os.path.normpath(line)))

                    copytree(line, str(copiedDirectory.absolute()))
                else:
                    raise ValueError('Invalid file or directory in input file: ' + line)

            # If destination directory exists, pass
            except OSError as e:
                if e.errno == 17:
                    pass
                else:
                    raise

        print('System backup completed')
        print('System backup location: ' + output)

