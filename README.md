# Python Scraper for World Athletics Database

## About

This is a python project that scrapes data from the World Athletics website and turns it into a large track and field csv dataset.

When executed it will take the current date as the end date and gather all the results for each track and field discipline.

Used the options.json file from that repo to help

Note: Datasets here were generated on: 2025-09-20

### Repo Structure

```

├── datasets
│   ├── split_by_discipline
│   ├── split_by_type
│   ├── all_disciplines_combined.csv
│   ├── individual_events.csv
│   └── relay_events.csv
├── docs
│   └── 0-todo.md
├── logs
│   └── 2025-12-24
├── processing
│   ├── combined
│   └── output
├── scripts
│   ├── combine.py
│   ├── preprocessing.py
│   ├── scraper_final.py
│   └── split_by_type.py
├── options.json
├── README.md
├── requirements.txt
└── run.py

```

### To Run

Install requirements from requirements.txt:

``` 
pip install -r requirements.txt
```

Run file "run.py":

``` 
python3 run.py
```

## Athletics Performance Dataset Description

This dataset contains structured performance records from international athletics competitions. Each row corresponds to an athlete's performance in a single event.

## Columns

| Column Name           | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `rank`                | Athlete’s placement within the discipline overall (1 = first place).                     |
| `mark`                | Performance mark (in seconds for track or meters for field events).         |
| `wind`                | Wind reading during the event (m/s); relevant for sprints and hurdles.      |
| `competitor`          | Full name of the athlete.                                                   |
| `dob`                 | Date of birth of the athlete (`YYYY-MM-DD`).                                |
| `nationality`         | 3-letter IOC code representing the athlete’s country.                       |
| `position`            | The athlete's position in the heat/final (if different from rank).          |
| `venue`               | Full name of the event venue.                                               |
| `date`                | Date of the event (`YYYY-MM-DD`).                                           |
| `result_score`        | Scoring index from the event, if available. Created by WAA, max of 1400                   |
| `discipline`          | Original discipline string, including implement or hurdle specs (e.g., `110m-hurdles-990cm`). |
| `type`                | General classification of the event (e.g., `sprints`, `hurdles`, `throws`). |
| `gender`              | Athlete's gender (`male` or `female`).                                      |
| `age_cat`        | Athlete's age classification (e.g., `u20`, `u18`, `senior`).                |
| `normalized_discpline`| Cleaned discipline name used for grouping (e.g., `110-metres-hurdles`).     |
| `track_field`         | Whether the event is a `track`, `field`, or `mixed` discipline.             |
| `mark_numeric`        | Parsed numeric value of the mark (in seconds or meters).                    |
| `venue_country`  | IOC 3-letter code extracted from the venue (e.g., `KEN`).                   |
| `age_at_event`        | Age of the athlete at the time of the event (in full years).                |
| `season`              | Year in which the event took place.                                         |

## Acknowledgement
Options.json file from: <https://github.com/thomascamminady/world-athletics-database/>
