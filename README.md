# google-maps-parser

## Getting started

Install all dependencies with:

```
pip install -r requirements.txt
```

> Note: This script requires Python 3.6+

## Usage:

An example query for searching famous museums in London can be:

```bash
python fetch.py --directory output/england/london --rating 4.5 --reviews 1000 --operator and --query "musuems in london"
```

This will return all the museums in London that have a rating > 4.5 *and* a review count > 1000. See more details with:

```
python fetch.py --help

usage: fetch.py [-h] [--query QUERY] [--directory DIRECTORY] [--rating RATING]
                [--reviews REVIEWS] [--operator {and,or}]
                [--exclude {park,point_of_interest,establishment,museum,library,church,art_gallery,political} [{park,point_of_interest,establishment,museum,library,church,art_gallery,political} ...]]
                [--language {en,fr,de}]

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
```

## Imorting to Google My Maps

The resulting CSV files can be imported to Google My Maps.
