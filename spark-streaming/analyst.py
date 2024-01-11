from pyspark.sql import SparkSession
from pyspark.sql.types import *
from datetime import datetime
from pyspark.sql.functions import *
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.0,'\
                                    'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,' \
                                    'com.mysql:mysql-connector-j:8.0.33,' \
                                    'org.apache.kafka:kafka-clients:3.6.0 pyspark-shell'

spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .master("local[*]") \
    .config("spark.jars.packages", "com.mysql:mysql-connector-j:8.0.33") \
    .getOrCreate()

df = spark\
    .readStream\
    .format('kafka') \
    .option('kafka.bootstrap.servers', 'kafka-1:9092,kafka-2:9092, kafka-3:9092') \
    .option('subscribe', 'Order') \
    .load()

schema = StructType([
    StructField("BDS_id", IntegerType(), nullable=True),
    StructField("time", DateType(), nullable=True),
    StructField("title", StringType(), nullable=True),
    StructField("poster_temp", StringType(), nullable=True),
    StructField("area_temp", StringType(), nullable=True),
    StructField("unit_temp", StringType(), nullable=True),
    StructField("price_temp", FloatType(), nullable=True),
    StructField("final_price", FloatType(), nullable=True)
])

df = df.selectExpr("CAST(value AS STRING)")

bds_df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# bds_df = bds_df.select(explode(col("data")).alias("bds_data")).select("bds_data.*")
# bds_df.printSchema()
# bds_df.writeStream.format('console').outputMode("append").start().awaitTermination()

bds_df = bds_df.withColumn("price_final", col("price_temp") * 1.1) \
    .withColumn("title_length", col("title").cast(IntegerType())) \
    .withColumn("poster_area", col("poster_temp") + " | " + col("area_temp"))
#-------------------------
price_ranges = [(0, 10000), (10000, 15000), (15000, 30000), (30000, float('inf'))]
labels = ['Low', 'Medium', 'High', 'Very High']

bds_df_with_range = bds_df.withColumn('price_range',
                                       when(col('final_price').between(price_ranges[0][0], price_ranges[0][1]), labels[0])
                                      .when(col('final_price').between(price_ranges[1][0], price_ranges[1][1]), labels[1])
                                      .when(col('final_price').between(price_ranges[2][0], price_ranges[2][1]), labels[2])
                                      .otherwise(labels[3]))

area_range = bds_df_with_range\
                    .groupby('area_temp', 'price_range')\
                    .agg(count('*').alias('property_count'))

def write_range_to_mysql(df, epoch_id):
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://mysql:3306/sales_db") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "area") \
        .option("user", "root") \
        .option("password", "secret") \
        .mode("append") \
        .save()

    print(epoch_id, "saved to mysql area table")
#------------------------
def write_to_mysql_original(df, epoch_id):
    df.write \
        .format("jdbc") \
        .option("url", "jdbc:mysql://mysql:3306/sales_db") \
        .option("driver", "com.mysql.cj.jdbc.Driver") \
        .option("dbtable", "sales") \
        .option("user", "root") \
        .option("password", "secret") \
        .mode("append") \
        .save()

    print(epoch_id, "saved to mysql sales table")


# Write the streaming DataFrame to MySQL using foreachBatch
query1 = bds_df\
    .writeStream \
    .trigger(processingTime="15 seconds") \
    .foreachBatch(write_to_mysql_original) \
    .outputMode("append") \
    .start()

query1.awaitTermination()

query2 = area_range\
    .writeStream \
    .trigger(processingTime="15 seconds") \
    .foreachBatch(write_range_to_mysql) \
    .outputMode("append") \
    .start()

query2.awaitTermination()