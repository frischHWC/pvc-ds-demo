from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import Row, StructField, StructType, StringType, IntegerType, BooleanType, DoubleType
from pyspark.sql.functions import col, udf
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.feature import StringIndexer
from pyspark.ml.classification import DecisionTreeClassificationModel
import json


# Create a Spark Session locally (to avoid spinning up executors)
spark = SparkSession\
    .builder\
    .appName("WeatherModel")\
    .master("local[*]")\
    .getOrCreate()

# Load Spark model from local FS
model_loaded = DecisionTreeClassificationModel.load("model_spark")
columns = ['wind_provenance_9_am' ,  'wind_force_9_am', "wind_provenance_9_pm", "wind_force_9_pm", "pressure_9_am", "pressure_9_pm","humidity_9_am", "humidity_9_pm", "temperature_9_am", "temperature_9_pm"]


def predict(input_dict):
    
    data = [(input_dict["wind_p_9_am"], input_dict["wind_f_9am"], input_dict["wind_p_9_pm"], input_dict["wind_f_9_pm"], input_dict["p_9am"], input_dict["p_9pm"], input_dict["h_9am"], input_dict["h_9pm"], input_dict["t_9am"], input_dict["t_9pm"])]

    df = spark.createDataFrame(data,columns)

    # Index wind_provenance columns (to transform string to int)
    df_index_wind_9am = StringIndexer(inputCol="wind_provenance_9_am", outputCol="wind_provenance_9_am_index").fit(df).transform(df)
    df_index_wind_9pm = StringIndexer(inputCol="wind_provenance_9_pm", outputCol="wind_provenance_9_pm_index").fit(df_index_wind_9am).transform(df_index_wind_9am)

    # Create features Vector
    vecAssembler = VectorAssembler(outputCol="features")
    vecAssembler.setInputCols(
      ["wind_force_9_am", "wind_force_9_pm", "pressure_9_am", "pressure_9_pm",
       "humidity_9_am", "humidity_9_pm", "temperature_9_am", "temperature_9_pm",
      "wind_provenance_9_pm_index", "wind_provenance_9_am_index"])
    vectorized = vecAssembler.transform(df_index_wind_9pm)

    # Predict the model
    predictions = model_loaded.transform(vectorized)

    # Return result
    raw_result = predictions.select("prediction").take(1)[0]['prediction']
    if raw_result <= 0.5:
      result = {"rain" : "no" }
    else:
      result = {"rain" : "yes" }

    return json.dumps(result)