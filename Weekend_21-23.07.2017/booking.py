#!/usr/bin/python3

import requests,json
import argparse as ap

'''
Validation of input data is not performed in this script,
so please provide correct IATA codes, valid dates and options according to task requirments.
'''

def parseArgs():

    argparser = ap.ArgumentParser()
    arggroup = argparser.add_mutually_exclusive_group()
    argparser.add_argument('-d','--date', type=str, help='the date of departure yyyy-mm-dd')
    argparser.add_argument('-f','--from', dest='departure', type=str, help='airport - IATA code')
    argparser.add_argument('-t','--to', dest='arrival', type=str, help='airport - IATA code')
    arggroup.add_argument('--one-way',  action='store_true')
    arggroup.add_argument('--cheapest', action='store_true')
    arggroup.add_argument('--shortest', action='store_true')
    arggroup.add_argument('--return', dest='nights', type=int, help='number of nights to stay in destination')
    args = argparser.parse_args()

    if not all((args.date, args.departure, args.arrival)):
        print ('No input data was provided.\nPlease use --help to see options.')
        return
    else:
        return args
        
        
def searchFlight(departure,arrival,dep_date,typeFlight,nightsToStay):
    search_url = 'https://api.skypicker.com/flights?v=3&limit=1'
    search_url += '&flyFrom='+departure+'&to='+arrival+'&dateFrom='+dep_date+'&typeFlight='+typeFlight+nightsToStay
    search_response = requests.get(search_url)
    if search_response.ok:
        flight = search_response.json()
        currency = flight['currency']
        bookingToken = flight['data'][0]['booking_token']
        return currency, bookingToken
    else:
        return 'Search request failed'

def bookFlight(curr, book_token):
    headers = {'Content-Type': 'application/json'}
    booking_url = 'http://37.139.6.125:8080/booking'
    bookingRequest = {"currency": curr,
                      "booking_token": book_token,
                      "passengers": {"birthday": "1917-01-01",
                                     "documentID": "PL123456",
                                     "lastName": "Mask",
                                     "firstName": "Elon",
                                     "title": "Mr",
                                     "email": "martian@spacex.future"}
                     }
        
    booking_response = requests.post(booking_url, headers=headers, json=bookingRequest)
    if booking_response.ok:
        booking_result = booking_response.json() 
        return booking_result['pnr']
    else:
        return 'Booking request failed'

def main():
    args = parseArgs()
    dep_date = '/'.join(args.date.split('-')[::-1])
    nightsToStay = ''
    if args.cheapest:
        typeFlight = 'cheapest'
    elif args.shortest:
        typeFlight = 'shortest'
    elif args.nights:
        typeFlight = 'return'
        nightsToStay = '&daysInDestinationFrom='+str(args.nights+1)+'&daysInDestinationTo='+str(args.nights+1)
    else:
        typeFlight = 'one-way'
    
    currency, bookingToken = searchFlight(args.departure,args.arrival,dep_date,typeFlight,nightsToStay)
    pnr = bookFlight(currency, bookingToken)
    print ('Your confirmation number is:',pnr)
    
if __name__ == "__main__":
    main()
