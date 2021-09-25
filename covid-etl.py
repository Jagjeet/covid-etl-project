import pandas as pd
import sqlalchemy
from config import pgUser, pgPassword

# EXTRACT
# import NY Times covid data
counties_df = pd.read_csv('data/us-counties.csv', dtype={'fips': str})
states_df = pd.read_csv('data/us-states.csv', dtype={'fips': str})
us_df = pd.read_csv('data/us.csv')

# import Census.gov population data
# Use truncated data as we only really need 2020 population estimates
county_est_df = pd.read_csv('data/co-est2020.csv', dtype={'STATE': str, 'COUNTY': str})

# TRANSFORM
# Break up state and county and reindex
county_pop_df = county_est_df.loc[county_est_df['COUNTY'] != '000'].copy()
county_pop_df = county_pop_df.reset_index(drop=True)

state_pop_df = county_est_df.loc[county_est_df['COUNTY'] == '000'].copy()
state_pop_df = state_pop_df.reset_index(drop=True)

# Drop non-2020 estimates (we only care about the latest)
county_pop_df = county_pop_df.drop(['CENSUS2010POP', 'ESTIMATESBASE2010', 'POPESTIMATE2010',
       'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013',
       'POPESTIMATE2014', 'POPESTIMATE2015', 'POPESTIMATE2016',
       'POPESTIMATE2017', 'POPESTIMATE2018', 'POPESTIMATE2019',
       'POPESTIMATE042020'], axis=1)

state_pop_df = state_pop_df.drop(['CENSUS2010POP', 'ESTIMATESBASE2010', 'POPESTIMATE2010',
       'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013',
       'POPESTIMATE2014', 'POPESTIMATE2015', 'POPESTIMATE2016',
       'POPESTIMATE2017', 'POPESTIMATE2018', 'POPESTIMATE2019',
       'POPESTIMATE042020'], axis=1)

# Add 5 digit FIPS column to county data
county_pop_df['FIPS'] = county_pop_df['STATE'] + county_pop_df['COUNTY']

# LOAD
# Create the engine to connect to the PostgreSQL database
connection_str = f"{pgUser}:{pgPassword}@localhost:5432/CovidDB"
engine = sqlalchemy.create_engine(f"postgresql://{connection_str}")

# Write data into the table in PostgreSQL database
county_pop_df.to_sql('population_us_counties',engine)
state_pop_df.to_sql('population_us_states',engine)
counties_df.to_sql('covid_us_counties',engine)
states_df.to_sql('covid_us_states',engine)
us_df.to_sql('covid_us',engine)