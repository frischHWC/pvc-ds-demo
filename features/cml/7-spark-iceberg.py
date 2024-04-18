from pyspark.sql import SparkSession, DataFrame
import time

# Create a Spark Session
spark = SparkSession\
  .builder\
  .appName("PlantsAndSensors")\
  .config("spark.jars", "/opt/spark/optional-lib/iceberg-spark-runtime.jar,/opt/spark/optional-lib/iceberg-hive-runtime.jar")\
  .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")\
  .config("spark.sql.catalog.spark_catalog.type", "hive")\
  .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog")\
  .config("spark.hadoop.iceberg.engine.hive.enabled", "true")\
  .getOrCreate()


# Read French speed sensors
df_bank_accounts = spark.read.parquet("/user/datagen/hdfs/banking/bank_account/")  
df_bank_accounts.printSchema()

# Create database if needed
spark.sql("CREATE DATABASE IF NOT EXISTS spark_ml_iceberg")

# Write as a table
df_bank_accounts.writeTo("spark_ml_iceberg.bank_accounts").using("iceberg").createOrReplace()

# Get timestamp
timestamp_before_deletion = int(time.time()*1000)

# Let's update and remove all our sensors that are placed in Paris
spark.sql(" DELETE FROM spark_ml_iceberg.bank_accounts WHERE city_of_residence = 'New York' ")

# Read History
historyDf = spark.sql("SELECT * FROM spark_ml_iceberg.bank_accounts.history")
historyDf.show()

# Now, count the number of rows in this table
spark.sql("SELECT count(*) FROM spark_ml_iceberg.bank_accounts").show()

# Time travel to read previous rows and print the count
df_speed_sensors_specific_date = spark.read.option("as-of-timestamp", str(timestamp_before_deletion)).format("iceberg").load("spark_ml_iceberg.bank_accounts")
df_speed_sensors_specific_date.show()

print('Count before deletion: ' + str(df_speed_sensors_specific_date.count()))


  