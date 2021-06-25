import csv
import sys
import getopt


class Color:
    def __init__(self):
        pass

    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def usage():
    note = "Default invocation: Specifying no options shifts the csv up two rows and\nremoves " \
           "50 columns from the right."
    shift_rows_up = "Shifts csv rows up by specified number of rows."
    shift_columns_left = "Removes specified number of columns from the right to the left."
    help = "Displays help menu."
    input_csv_filename = "Input file name of CSV." + Color.BOLD + Color.YELLOW + " REQUIRED" + Color.END
    options = [Color.BOLD + '-i ' + Color.END + Color.UNDERLINE + "<filename>" + Color.END,
               Color.BOLD + '-r ' + Color.END + Color.UNDERLINE + "<rows>" + Color.END,
               Color.BOLD + '-c ' + Color.END + Color.UNDERLINE + "<columns>" + Color.END,
               Color.BOLD + '-h ' + Color.END]
    long_options = [Color.BOLD + '--input-csv-filename ' + Color.END + Color.UNDERLINE + "<filename>" + Color.END,
                    Color.BOLD + '--shift-rows-up ' + Color.END + Color.UNDERLINE + "<rows>" + Color.END,
                    Color.BOLD + '--shift-columns-left ' + Color.END + Color.UNDERLINE + "<columns>" + Color.END,
                    Color.BOLD + '--display-help' + Color.END]
    descriptions = [input_csv_filename, shift_rows_up, shift_columns_left, help]

    print(Color.BOLD + "--usage menu--\nFormatCSV\n" + Color.END + note + "\n\nOptional invocations")
    print(Color.BOLD + "python3 FormatCSV.py " + Color.END + options[0] + ' ' + options[1] + ' ' + options[2] + ' ' + options[3])
    for i in range(len(options)):
        print("\t{:<30}\t{}".format(options[i], descriptions[i]))

    print("\nLong name invocations\n" + Color.BOLD + "python3 FormatCSV.py " + Color.END + long_options[0] + ' ' +
          long_options[1] + ' ' + long_options[2] + ' ' + long_options[3])
    for i in range(len(long_options)):
        print("\t{:<50}{}".format(long_options[i], descriptions[i]))


def parse_parameters(argv):
    try:
        opts, args = getopt.getopt(argv, "i:r:c:h", ["input-csv-filename=", "shift-rows-up=", "shift-columns-left=",
                                                     "display-help"])
    except getopt.GetoptError as err:
        print(Color.BOLD + Color.YELLOW + str(err) + Color.END)
        usage()
        sys.exit(2)
    shift_rows_up = 0
    shift_columns_left = 0
    input_file = False
    rows_specified = False
    columns_specified = False
    for opt, arg in opts:
        if opt in ("-h", "--display-help"):
            usage()
            sys.exit()
        elif opt in ("-i", "--input-csv-filename"):
            input_file = arg
        elif opt in ("-c", "--shift-columns-left"):
            if not arg.isdigit():
                print(Color.BOLD + Color.YELLOW + "'{}' is not a number".format(arg) + Color.END)
                sys.exit(1)
            shift_columns_left = int(arg)
            columns_specified = True
        elif opt in ("-r", "--shift-rows-up"):
            if not arg.isdigit():
                print(Color.BOLD + Color.YELLOW + "'{}' is not a number".format(arg) + Color.END)
                sys.exit(1)
            shift_rows_up = int(arg)
            rows_specified = True
    if not input_file:
        print(Color.BOLD + Color.YELLOW + "option -i requires argument" + Color.END)
        usage()
        sys.exit(1)
    if not rows_specified:
        print("Setting shift_rows_up to 2 - Default invocation")
        shift_rows_up = 2
    if not columns_specified:
        print("Setting shift_columns_left to 50 - Default invocation")
        shift_columns_left = 50
    return input_file, shift_rows_up, shift_columns_left


def format_csv(input_file, shift_rows_up, shift_columns_left):
    new_csv = []
    try:
        with open(input_file, 'r') as f:
            csv_num_rows = csv.reader(f)
            num_rows = len(list(csv_num_rows))
            if int(num_rows) <= int(shift_rows_up):
                print(Color.BOLD + Color.YELLOW + "'{}' is greater than the number of "
                                                  "rows ({})".format(shift_rows_up, num_rows) + Color.END)
                sys.exit(1)
            f.close()
        with open(input_file, 'r') as f:
            csv_r = csv.reader(f)
            for row in csv_r:
                if len(row) <= shift_columns_left:
                    print(Color.BOLD + Color.YELLOW + "'{}' is greater than the number of "
                                                      "columns ({})".format(shift_columns_left, len(row)) + Color.END)
                    sys.exit(1)
                if shift_rows_up < 1:
                    new_csv.append(row)
                shift_rows_up -= 1
            for row in new_csv:
                shift = shift_columns_left
                for i in range(shift):
                    row.pop()
            f.close()
        with open(input_file, 'w') as f:
            csv_w = csv.writer(f)
            for row in new_csv:
                csv_w.writerow(row)
            f.close()
    except IOError as err:
        print(Color.BOLD + Color.YELLOW + str(err) + Color.END)
        sys.exit(-1)


def main(argv):
    input_file, shift_rows_up, shift_columns_left = parse_parameters(argv)
    format_csv(input_file, shift_rows_up, shift_columns_left)


if __name__ == "__main__":
    main(sys.argv[1:])
