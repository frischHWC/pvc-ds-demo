from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import Row
from pyspark.sql.functions import col
from pyspark.sql.functions import sum as _sum
import time


def main(spark):  
  
  # Read French speed sensors
  df_france_speed_sensors_data = spark.read.parquet("/user/datagen/hdfs/industry/sensor_french_speed_data/")  
  df_france_speed_sensors_data.printSchema()

  # Create database if needed
  spark.sql("CREATE DATABASE IF NOT EXISTS spark_iceberg")
  
  # Write as a table
  df_france_speed_sensors_data.writeTo("spark_iceberg.french_sensors").using("iceberg").createOrReplace()

  # Get timestamp
  timestamp_before_deletion = int(time.time()*1000)

  # Let's update and remove all our sensors that are placed in Paris
  spark.sql(" DELETE FROM spark_iceberg.french_sensors WHERE city = 'Paris' ")

  # Read History
  historyDf = spark.sql("SELECT * FROM spark_iceberg.french_sensors.history")
  historyDf.show()

  # Now, count the number of rows in this table
  spark.sql("SELECT count(*) FROM spark_iceberg.french_sensors").show()

  # Time travel to read previous rows and print the count
  df_speed_sensors_specific_date = spark.read.option("as-of-timestamp", str(timestamp_before_deletion)).format("iceberg").load("spark_iceberg.french_sensors")
  df_speed_sensors_specific_date.show()

  print('Count before deletion: ' + str(df_speed_sensors_specific_date.count()))


if __name__ == '__main__':
  # Create a Spark Session
  spark = SparkSession\
  .builder\
  .appName("PlantsAndSensors")\
  .getOrCreate()
  
  main(spark)
  