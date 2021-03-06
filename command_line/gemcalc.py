#!/usr/bin/env python
#
# Love Gem (aka loveca) calculator
#
# Part of SIFTools <https://github.com/dburr/SIFTools/>
# By Donald Burr <dburr@DonaldBurr.com>
# Copyright (c) 2015 Donald Burr.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys
import getopt
import calendar
import datetime
from datetime import timedelta

def is_muse_members_birthday(month, day):
    is_bday = False
    bday_name = None
    if month == 1 and day == 17:
        is_bday = True
        bday_name = "Hanayo"
    elif month == 3 and day == 15:
        is_bday = True
        bday_name = "Umi"
    elif month == 4 and day == 19:
        is_bday = True
        bday_name = "Maki"
    elif month == 6 and day == 9:
        is_bday = True
        bday_name = "Nozomi"
    elif month == 7 and day == 22:
        is_bday = True
        bday_name = "Nico"
    elif month == 8 and day == 3:
        is_bday = True
        bday_name = "Honoka"
    elif month == 9 and day == 12:
        is_bday = True
        bday_name = "Kotori"
    elif month == 10 and day == 21:
        is_bday = True
        bday_name = "Eli"
    elif month == 11 and day == 1:
        is_bday = True
        bday_name = "Rin"
    return (is_bday, bday_name)

def is_gem_day(day):
    # according the login bonus chart, gems are given out on days numbered 1,6,11,16,21,26,30
    if day == 1 or day == 6 or day == 11 or day == 16 or day == 21 or day == 26 or day == 30:
        return True
    else:
        return False

def validate(date_text):
    try:
        datetime.datetime.strptime(date_text, '%m/%d/%Y')
        return True
    except ValueError:
        raise ValueError("Incorrect date format, should be MM/DD/YYYY")

def calc_gems_on_date(current_gems, target_date, verbose=False):
    now = datetime.datetime.now()
    target_datetime = datetime.datetime.strptime(target_date, '%m/%d/%Y')
    print "Today is %02d/%02d/%04d and you currently have %d love gems." % (now.month, now.day, now.year, current_gems)
    print "(Assuming you collected any gems you got today and already counted those.)"
    gems = current_gems
    now = now + timedelta(days=1)
    while now < target_datetime:
        if is_gem_day(now.day):
            gems = gems + 1
        (is_bday, name) = is_muse_members_birthday(now.month, now.day)
        if is_bday:
            gems = gems + 5
        if verbose:
            if is_gem_day(now.day) and is_bday:
                print "%02d/%02d/%04d: free gem as login bonus AND it's %s's birthday! You get 6 gems, which brings you to %d gems." % (now.month, now.day, now.year, name, gems)
            elif is_gem_day(now.day):
                print "%02d/%02d/%04d: free gem as login bonus, which brings you to %d gems." % (now.month, now.day, now.year, gems)
            elif is_bday:
                print "%02d/%02d/%04d: it's %s's birthday! You get 5 gems, which brings you to %d gems." % (now.month, now.day, now.year, name, gems)
        now = now + timedelta(days=1)
    print "You will have %d love gems on %02d/%02d/%04d. Good things come to those who wait!" % (gems, target_datetime.month, target_datetime.day, target_datetime.year)

def calc_desired_gems(current_gems, desired_gems, verbose=False):
    now = datetime.datetime.now()
    print "Today is %02d/%02d/%04d and you currently have %d love gems." % (now.month, now.day, now.year, current_gems)
    print "(Assuming you collected any gems you got today and already counted those.)"
    gems = current_gems
    while gems < desired_gems:
        now = now + timedelta(days=1)
        if is_gem_day(now.day):
            gems = gems + 1
        (is_bday, name) = is_muse_members_birthday(now.month, now.day)
        if is_bday:
            gems = gems + 5
        if verbose:
            if is_gem_day(now.day) and is_bday:
                print "%02d/%02d/%04d: free gem as login bonus AND it's %s's birthday! You get 6 gems, which brings you to %d gems." % (now.month, now.day, now.year, name, gems)
            elif is_gem_day(now.day):
                print "%02d/%02d/%04d: free gem as login bonus, which brings you to %d gems." % (now.month, now.day, now.year, gems)
            elif is_bday:
                print "%02d/%02d/%04d: it's %s's birthday! You get 5 gems, which brings you to %d gems." % (now.month, now.day, now.year, name, gems)
    print "You will have %d love gems on %02d/%02d/%04d. Good things come to those who wait!" % (gems, now.month, now.day, now.year)
    
def usage():
    print "Usage: %s [options]" % os.path.basename(__file__)
    print "where [options] can be one or more of:"
    print "[-H | --help]          Print this help message"
    print "[-g | --current-gems]  Current number of love gems (optional, default=0)"
    print "[-v | --verbose]       Verbosely print out when gems are collected"
    print ""
    print "Plus one of the following:"
    print ""
    print "TO CALCULATE NUMBER OF LOVE GEMS YOU'LL HAVE ON A GIVEN DATE:"
    print "[-d | --date]          Date to calculate gem count for (MM/DD/YYYY)"
    print ""
    print "TO CALCULATE HOW LONG UNTIL YOU WILL GET A CERTAIN NUMBER OF GEMS:"
    print "[-G | --desired-gems]  Calculate date when you will have that number of gems"

def main(argv):
    current_gems = 0
    target_date = None
    desired_gems = None
    verbose = False
    try:                                
        options, remainder = getopt.getopt(argv, "Hg:d:G:v", ["help", "current-gems=", "date=", "desired-gems=", "verbose"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)                     
    for opt, arg in options:
        if opt in ('-H', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-g', '--current-gems'):
            current_gems = int(arg)
        elif opt in ('-d', '--date'):
            target_date = arg
        elif opt in ('-G', '--desired-gems'):
            desired_gems = int(arg)
        elif opt in ('-v', '--verbose'):
            verbose = True

    # now do something
    if target_date is not None:
        # validate it
        if validate(target_date):
            calc_gems_on_date(current_gems, target_date, verbose)
    elif desired_gems is not None:
        if desired_gems <= current_gems:
            print "Error: desired gems must be greater than current gems"
            usage()
            sys.exit(0)
        else:
            calc_desired_gems(current_gems, desired_gems, verbose)
    else:
        print "Error: must specify either -d or -G."
        usage()
        sys.exit(2)

### main script starts here

if __name__ == "__main__":
    main(sys.argv[1:])