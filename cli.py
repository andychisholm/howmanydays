import sys

from dates import to_date, get_days_between


def parse_date_string(ds):
    """
    Parses a date string into an internal date representation.

    :param ds: a string encoded date like "21/01/2017"
    :return: a date object
    """
    if not ds or not isinstance(ds, str):
        raise ValueError("Expected non-empty string for date")

    # validate our date string
    parts = ds.split('/')
    if len(parts) != 3:
        raise ValueError("Expecting three parts to the date string separated by a '/'")
    for p in parts:
        if not p.isdigit():
            raise ValueError("Date parts should be integers")

    # pull out the components
    day, month, year = [int(p) for p in parts]

    # blow up at this point if the parsed date is invalid
    return to_date(day, month, year)


def main(args=sys.argv[1:]):
    if len(args) != 2:
        print("Run me like:\n\tpython %s dd/mm/yyyy dd/mm/yyyy" % sys.argv[0])
        exit()

    a, b = args
    try:
        a_date = parse_date_string(a)
    except ValueError as ve:
        print(a, ve.message)
        exit()

    try:
        b_date = parse_date_string(b)
    except ValueError as ve:
        print(b, ve.message)
        exit()

    print(get_days_between(a_date, b_date))


if __name__ == '__main__':
    main()
