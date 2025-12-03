#!/usr/bin/env python3
import sys
import antigravity


def main():
    if len(sys.argv) != 4:
        print("Usage: python geohashing.py <latitude> <longitude> <datedow>")
        sys.exit(1)

    if len(sys.argv[3]) != 8:
        print("Error: datedow must be 8 characters long (YYYYMMDD)")
        sys.exit(1)

    if (
        not sys.argv[1].replace(".", "", 1).isdigit()
        or not sys.argv[2].replace(".", "", 1).isdigit()
    ):
        print("Error: latitude and longitude must be valid numbers")
        sys.exit(1)

    print(
        "Geohashing with latitude:",
        sys.argv[1],
        "longitude:",
        sys.argv[2],
        "datedow:",
        sys.argv[3],
    )
    try:
        latitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        datedow = sys.argv[3].encode()
        antigravity.geohash(latitude, longitude, datedow)
    except ValueError:
        print("Error: latitude and longitude must be numbers")
        sys.exit(1)


if __name__ == "__main__":
    main()
