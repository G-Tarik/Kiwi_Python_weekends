#!/usr/bin/bash
./book_flight.py --date 2017-10-13 --from BCN --to DUB --one-way
./book_flight.py --date 2017-10-13 --from LHR --to DXB --return 5
./book_flight.py --date 2017-10-13 --from NRT --to SYD --cheapest
./book_flight.py --date 2017-10-13 --from CPH --to MIA --shortest

