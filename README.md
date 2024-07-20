# MBTA Route Lengths

This is code to calculate the length of MBTA routes from GTFS bundles. The output takes the form of a JSON file with this structure:

```json
{
    "Green-B": [
        {
            "from_station_id": "place-lake",
            "to_station_id": "place-sougr",
            "from_station_name": "Boston College",
            "to_station_name": "South Street",
            "distance": 0.76
        },
        {
            "from_station_id": "place-sougr",
            "to_station_id": "place-chill",
            "from_station_name": "South Street",
            "to_station_name": "Chestnut Hill Avenue",
            "distance": 0.45
        },
        ...
    ],
    "Green-C": [
        ...
    ],
    ...
}
```

## Installing

Requirements:

- Python 3.8+
- [Python Poetry](https://python-poetry.org/)

To install dependencies:

```bash
poetry install
```

## Configuring the script

To configure the script, copy `config.example.json` to `config.json` and edit the values as needed.

- `feedsPath` is a path to any directory on your computer where you'd like to hold a cache of GTFS bundles. The script will automatically download them and store them here. Other TM tools use this same directory, so if you already have it set up, you can use the same path.
- `targetRouteIds` is a list of route IDs to calculate the length of. You can find a list of route IDs in the `routes.txt` file in any GTFS bundle.

Here's an example `config.json`:

```json
{
    "feedsPath": "~/path/to/feeds/somewhere",
    "targetRouteIds": [
        "Green-B",
        "Green-C",
        "Green-D",
        "Green-E"
    ]
}
```

You can use the special value `"*"` to query all route IDs.

## Running the script

To run the script, run this command:

```bash
make run
```

This might take a while to run the first time, since it has to download a GTFS bundle. Subsequent runs will be faster.
