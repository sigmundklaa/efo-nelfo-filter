
import csv
from pathlib import Path


ENCODING = 'ISO-8859-1'
CSV_ARGS = {'delimiter': ';', 'quoting': csv.QUOTE_NONE, 'quotechar': None}


def main(inp: Path, out: Path, logfile: Path) -> None:
    with open(inp, encoding=ENCODING) as ifp, \
            open(out, 'w', encoding=ENCODING) as ofp, \
            open(logfile, 'w', encoding=ENCODING) as fp:

        reader = csv.reader(ifp, **CSV_ARGS)
        writer = csv.writer(ofp, **CSV_ARGS)
        logger = csv.writer(fp, **CSV_ARGS)

        nvl_add = nvl_del = 0
        deleted = False

        for idx, line in enumerate(reader):
            head = line[0].upper()
            is_vl = head == 'VL'

            if deleted:
                if head in ('VH', 'VL'):
                    deleted = False
            if is_vl and int(line[8]) == 0:
                deleted = True

            if deleted:
                logger.writerow([idx] + line)
                nvl_del += is_vl
            else:
                writer.writerow(line)
                nvl_add += is_vl

        print(f'VL Added: {nvl_add}, VL Removed {nvl_del}')


if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, help='File to read')
    parser.add_argument('-o', '--output', type=str, default='./out.csv',
                        help='Path to output')
    parser.add_argument('-l', '--logfile', type=str,
                        default='./log.csv', help='Path to logfile')

    opts = parser.parse_args(sys.argv[1:])

    main(inp=Path(opts.file), out=Path(opts.output), logfile=Path(opts.logfile))
