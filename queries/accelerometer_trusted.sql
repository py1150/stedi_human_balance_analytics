CREATE EXTERNAL TABLE `acelerometer_trusted`(
  `user` string COMMENT 'from deserializer', 
  `timestamp` bigint COMMENT 'from deserializer', 
  `x` double COMMENT 'from deserializer', 
  `y` double COMMENT 'from deserializer', 
  `z` double COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://p3-stedi-lakehouse/accelerometer/trusted/'
TBLPROPERTIES (
  'CreatedByJob'='accelerometer_landing_to_trusted', 
  'CreatedByJobRun'='jr_faebb4de287717dc538de87c0039024b0a5cbf59d634b3ddbc6911137d19982d', 
  'classification'='json')