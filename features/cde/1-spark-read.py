from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import Row
from pyspark.sql.functions import col
from pyspark.sql.functions import sum as _sum


def main(spark):  
  
  # Read French speed sensors and group them by city
  df_france_speed_sensors_data = spark.read.parquet("/user/datagen/hdfs/industry/sensor_french_speed_data/")  
  df_france_speed_sensors_data.printSchema()
  df_france_speed_sensors_data.groupBy("city")\
  .agg(_sum("value").alias("sum_values")).orderBy(col("sum_values").desc()).show()
  
  
if __name__ == '__main__':
  # Create a Spark Session
  spark = SparkSession\
  .builder\
  .appName("PlantsAndSensors")\
  .getOrCreate()
  
  main(spark)