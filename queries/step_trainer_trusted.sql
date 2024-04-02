CREATE EXTERNAL TABLE `step_trainer_trusted`(
  `sensorreadingtime` bigint COMMENT 'from deserializer', 
  `serialnumber` string COMMENT 'from deserializer', 
  `distancefromobject` int COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://p3-stedi-lakehouse/step_trainer/trusted/'
TBLPROPERTIES (
  'CreatedByJob'='step_trainer_landing_to_trusted', 
  'CreatedByJobRun'='jr_fa72e09f77561683b5b03c9f11c63a2eb694e5de9e118bac9ffe43dcac189bc5', 
  'classification'='json')