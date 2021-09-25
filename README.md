# covid-etl-project

This project extracts, transforms and loads Covid data from NY Times with county, state, and US population data taken from Census.gov in Postgres tables. A high level view can be found in the linked [presentation](https://docs.google.com/presentation/d/1K-bi7V2eI63Y3zEpxU2qML6Pc2YXFOa5xIRoxgjt230/edit?usp=sharing)

Data sources are below:

* [Covid-19 Data](https://github.com/nytimes/covid-19-data) - Covid-19 deaths and cases for the US tracked nationally, at the state level and by county
* [2010-2019 County Population Data](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-counties-total.html#par_textimage_739801612) - County Population Data
* State Population Data - Same as County
* National Population Data TBD -Yearly estimate not found as a CSV, but could be calculated from state if necessary.

Additionally it maybe helpful to reference [2020 FIPS Codes](https://www.census.gov/geographies/reference-files/2020/demo/popest/2020-fips.html) to automate transforming FIPS codes in the data to county names. Currently these are not used as they are included in the census data, but maybe used in the future.

## Prerequisites

To run this project the following tools are needed:

* Python (tested with v3.85, earlier versions may work as well, but have not been tested)
* Jupyter Notebooks and/or Jupyter Labs
* Anaconda is recommended though library dependencies can be installed individually as well.
* PostgreSQL
* Curl

## Usage

* Clone the repository
* Download the covid data by running `covid_data_download.sh` in a shell
* Download the population data by running `population_data_download.sh` in a shell
* Rename `config.py.sample` to `config.py`. Add your own username (`pgUser`) and password (`pgPassword`) for postgres.
* Run `python covid-etl.py` to extract the CSV data, transform it and load it into tables

Note the `covid-etl.ipynb` contains a playground for the ETL process. Further exploration can be done there and added to the final process as needed.

## Extract Details

As all the data was CSV based, the extract process is as simple as loading the CSVs once they are downloaded using the scripts provided.
## Transform Details

Highlights of transforming the data include

* Breaking up state and county population data and reindex. Since the Covid data is separated by US, State and County, it is helpful to have the population data available structured similarly.
* Drop non-2020 estimates. Since Covid occured in 2020, we only care about the latest estimates. Longer term 2021 and later data will be added.
* Add 5 digit FIPS column to county data in the population data to use the same FIPS structure as the Covid data uses.

## Load Details

The following tables are generated as part of the load process:

* covid_us - US national data for Covid cases and deaths
* covid_us_counties - County data for Covid cases and deaths
* covid_us_states - State data for Covid cases and deaths
* population_us_counties - US County Population estimates based on the 2010 census data
* population_us_states - US State Population estimates based on the 2010 census data


## Known Issues

* Population estimates were only available through 2020 for the moment
* National population estimates were not found for 2020 as a CSV. A constant could be used or the sum of the states could also be used instead of a separate one item table.
* In some cases data from previous Jupyter cells are used to calculate values in the current cell. As such make sure to run all above cells to obtain the correct output
* Ideally the user could specify the Postgres port too

## References

* [Resolving "pg-config" Executable Not Found On a Mac](https://stackoverflow.com/questions/20170895/mac-virtualenv-pip-postgresql-error-pg-config-executable-not-found)
* [Change Column Type in Pandas](https://stackoverflow.com/questions/15891038/change-column-type-in-pandas)
* [Show All Columns in Pandas Dataframe](https://stackoverflow.com/questions/49188960/how-to-show-all-columns-names-on-a-large-pandas-dataframe)
* [Specifying Data Type In Pandas CSV Reader](https://stackoverflow.com/questions/10591000/specifying-data-type-in-pandas-csv-reader)
* [Dropping Data Tables From SQLAlchemy](https://stackoverflow.com/questions/33229140/how-do-i-drop-a-table-in-sqlalchemy-when-i-dont-have-a-table-object/37095265)