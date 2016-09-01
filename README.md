# Zip Code Hardiness Zones

## About
The script uses the data from the [Open Plant Hardiness Zones(OPHZ)](https://github.com/wboykinm/ophz) and a [list of zip codes](https://gist.github.com/erichurst/7882666) with their latitude and longitude to create a csv dataset which maps a zip code to its plant hardiness zone.

## Input Format
The script requires the OPHZ shape file, and a csv file with the format [Label , Latitude, Longitude].

## Output Format
A CSV file is outputted which contains the label from the input CSV file, and the hardiness zone from the OPHZ shape file in the format [Label, Zone].
