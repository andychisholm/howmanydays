# these constants are good for earth, if elon makes it to mars we should revisit
DAYS_PER_YEAR = 365
LEAP_MONTH = 2

# list of the days for each calendar month from january to december
DAYS_BY_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# precompute the offset from the first day of the year to each month
OFFSET_BY_MONTH = [0]
for i, ds in enumerate(DAYS_BY_MONTH[:-1]):
    OFFSET_BY_MONTH.append(ds+OFFSET_BY_MONTH[i])


def _is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0


def _year_to_offset(year):
    # this is the number of years since an arbitrary epoch year
    # in this case, we take the year "0" to simplify calculations, though any year N : N%400==0 would do
    delta = year - 1
    return delta * DAYS_PER_YEAR + (delta // 4) - (delta // 100) + (delta // 400)


def _date_to_day_offset(date):
    """
    Converts a date representation to an offset from a fixed and arbitrary epoch.

    :param date: a date representation.
    :return: the number of days from the epoch.
    """
    year, month, day = date

    offset = day
    offset += OFFSET_BY_MONTH[month-1]
    offset += _year_to_offset(year)

    # add an extra day if this is a leap year
    if _is_leap_year(year) and month > LEAP_MONTH:
        offset += 1

    return offset


def to_date(day, month, year):
    """
    Returns a date object given valid date params, otherwise throws an exception.

    :param day: the day of the month represented as an integer
    :param month: the month of the year as an integer
    :param year: the year as an integer
    :return: an object representing the date
    """
    # validate the input types
    if not (isinstance(day, int) and isinstance(month, int) and isinstance(year, int)):
        raise ValueError("Expected integers for year, month and day")

    # validate the month
    if month < 1 or month > len(DAYS_BY_MONTH):
        raise ValueError("Invalid month")

    max_day = DAYS_BY_MONTH[month - 1]
    if _is_leap_year(year) and month == LEAP_MONTH:
        max_day += 1

    # validate the day of the month
    if day < 1 or day > max_day:
        raise ValueError("Expected a day between 1 and %d for a month of %d in %d" % (max_day, month, year))

    # we represent dates internally as a simple tuple
    # if we later needed to replace this with something more complicated later
    # e.g. a object of some date class, our api doesn't need to change
    return year, month, day


def get_days_between(frm, to):
    """
    Computes the number of days between two date representations.

    :param frm: the date we count days from
    :param to: the date we count day up-to but not including
    :return: the number of days between, or 0 if 'to' is not after 'from'
    """
    delta = _date_to_day_offset(to) - _date_to_day_offset(frm)
    if delta > 0:
        delta -= 1
    else:
        delta = 0
    return delta
