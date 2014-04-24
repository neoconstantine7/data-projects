import pandas
import pandasql


#return how many days there was rain from the dataset
def num_rainy_days(filename):

    weather_data = pandas.read_csv(filename)

    q = """
    SELECT COUNT(*)
    FROM weather_data
    WHERE rain=1;
    
    """
    
    #Execute your SQL command against the pandas frame
    rainy_days = pandasql.sqldf(q.lower(), locals())
    return rainy_days

def max_temp_aggregate_by_fog(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return two columns and
    two rows - whether it was foggy or not (0 or 1) and the max
    maxtempi for that fog value (i.e., the maximum max temperature
    for both foggy and non-foggy days). 
    '''

    weather_data = pandas.read_csv(filename)

    q = """
    SELECT fog, max(cast (maxtempi as integer))
    FROM weather_data
    GROUP BY fog
    """
    
    #Execute your SQL command against the pandas frame
    rainy_days = pandasql.sqldf(q.lower(), locals())
    return rainy_days 

def avg_temperature_weekends(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data.  The SQL query should return one column and
    one row - the average meantempi on days that are a Saturday
    or Sunday (i.e., the the average mean temperature on weekends).
    The dataframe will be titled 'weather_data' and you can access
    the date in the dataframe via the 'date' column.
    
    Also, you can convert dates to days of the week via the 'strftime' keyword in SQL.
    For example, cast (strftime('%w', date) as integer) will return 0 if the date
    is a Sunday or 6 if the date is a Saturday.
    
    '''
    weather_data = pandas.read_csv(filename)

    q = """
    SELECT AVG(cast (meantempi as integer))
    FROM weather_data
    WHERE cast(strftime('%w', date) as integer) =0 OR cast(strftime('%w', date) as integer)=6
    
    """
    
    #Execute your SQL command against the pandas frame
    mean_temp_weekends = pandasql.sqldf(q.lower(), locals())
    return mean_temp_weekends

def avg_min_temperature_over_55(filename):
    '''
    This function should run a SQL query on a dataframe of
    weather data. More specifically you want to find the average
    minimum temperature on rainy days where the minimum temperature
    is greater than 55 degrees.
    '''
    weather_data = pandas.read_csv(filename)

    q = """
    SELECT avg(cast (mintempi as integer))
    FROM weather_data
    WHERE mintempi>55 AND rain=1
    """
    
    #Execute your SQL command against the pandas frame
    mean_temp_weekends = pandasql.sqldf(q.lower(), locals())
    return mean_temp_weekends  

csv_data='weather_underground.csv'
print num_rainy_days(csv_data)
print max_temp_aggregate_by_fog(csv_data)
print avg_temperature_weekends(csv_data)
print avg_min_temperature_over_55(csv_data)
  