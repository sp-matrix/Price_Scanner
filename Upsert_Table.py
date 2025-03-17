# upsert_table.py
from pyspark.sql import SparkSession
import sys

if len(sys.argv) > 1:
    input_value = sys.argv[1]
else:
    raise ValueError("No input value provided")

spark = SparkSession.builder.appName("WriteToTable").getOrCreate()
data = [(input_value,)]
columns = ["value"]
df = spark.createDataFrame(data, columns)
df.write.mode("append").saveAsTable("your_table_name")
spark.stop()
""", True)
