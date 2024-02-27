# Data profileing application

This project is a final year dissertation project where the goal is to develop an application to allow a user to profile a new dataset with no code.

## Datasets

- [] backend
  - [x] load in dataset
    - [x] csv
    - [x] excel
    - [x] json
  - [x] Check for missing data
    - [x] check which collumns have missing data
    - [x] check which rows have missing data
  - [x] check data types
    - [x] numerical
      - [x] integer
      - [x] float
    - [x] string
    - [x] datetime
    - [x] char
    - [] other
  - [] checks for unique data
    - [] counts number of unique values in each column
  - [x] check for duplicates
    - [x] check by row
    - [] check by column
  - [] check for out of range
    - [] obvious ranges (number of days in month or number of hours in day)
    - [] user defined ranges
  - [] check for format issues
    - [] obvious formats (phone numbers, post codes)
    - [] user defined formats
- [] frontend
  - [] data input
    - [] drag and drop
  - [] data visualisations
    - [] rate data overall (based on missing, duplecates)
    - [] show some observations about data (number of types, number of unique collumns/rows)
    - [] color blind friendly
    - [] high value visualisations following heuristic rules
