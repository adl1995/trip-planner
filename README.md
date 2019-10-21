# google-maps-parser

This tool filters Google Maps places based on an input query and exports them to a CSV file. 

## Getting started

- Install all dependencies with:

```
$ pip install -r requirements.txt
```

- Rename the file `secrets.ini.example` to `secrets.ini` and add the Google Maps API key.
> Note: This script requires Python 3.6+

## Usage example

For fetching a list of attractions in London, we can do:

```
$ python fetch.py --directory output/england/london --rating 4.5 --reviews 5000 --operator and --query "attractions in London"
```

This will return all the attractions in London that have a rating >= 4.5 *and* a review count >= 5000. The output will contain the following columns:

```
| name                | coordinates                       | types                                                 | rating  | formatted address                                                                                 | summary                                                                                                                                                                                                                             | url                                           | reviews   |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
|-------------------- |---------------------------------  |------------------------------------------------------ |-------- |-------------------------------------------------------------------------------------------------  |-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  |---------------------------------------------- |---------  |---  |---  |---  |---  |---  |---  |---  |---  |---  |---  |---  |---  |---  |---  |---  |
| The London Dungeon  | (51.50251189999999, -0.1187628)   | tourist_attraction, point_of_interest, establishment  | 4.2     | Riverside Building, County Hall, Westminster Bridge Rd, Lambeth, London SE1 7PB, United Kingdom   | The London Dungeon is a tourist attraction along London's South Bank, England, which recreates various gory and macabre historical events in a gallows humour style. It uses a mixture of live actors, special effects and rides.   | https://en.wikipedia.org/wiki/London_Dungeon  | 11713     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
```

This file can then be imported to Google My Maps, which is described in the [section](#Imorting-to-Google-My-Maps) below.

### Refining a search query

Items can be exluded from a search query using the `--exclude` parameter. Considering our previous example, if we want to exlude all parks from our search query, the command can be modified as:

```
$ python fetch.py --directory output/england/london --rating 4.5 --reviews 5000 --operator and --query "attractions in London" --exclude park
```

More details can be viewed with the `--help` parameter:

```
$ python fetch.py --help

usage: fetch.py [-h] [--query QUERY] [--directory DIRECTORY] [--rating RATING]
                [--reviews REVIEWS] [--operator {and,or}]
                [--exclude {park,point_of_interest,establishment,museum,library,church,art_gallery,political} [{park,point_of_interest,establishment,museum,library,church,art_gallery,political} ...]]
                [--language {en,fr,de}] [--summary-length SUMMARY_LENGTH]

optional arguments:
  -h, --help            show this help message and exit
  --query QUERY         Search query for Google Maps API
  --directory DIRECTORY
                        Output directory
  --rating RATING       Minimum rating of the place(s)
  --reviews REVIEWS     Minimum review count of the place(s)
  --operator {and,or}   Operation to perform between ratings and reviews
                        count.
  --exclude {park,point_of_interest,establishment,museum,library,church,art_gallery,political} 
                        Exclude the places from the query result
  --language {en,fr,de}
                        Language of the Wikipedia link
  --summary-length SUMMARY_LENGTH
                        Limit the number of sentences in place summary.
```

## Imorting to Google My Maps

The following blog post describes how the CSV files can be imported to Google My Maps.
- [Programmatically organising your backpacking trip using Google My Maps](https://adl1995.github.io/programmatically-organising-your-backpacking-trip-using-google-my-maps.html)
