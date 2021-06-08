# Streaming Finance Data with AWS Lambda

This project consists of 3 major infrastructure elements, a lambda function that gathers stock data on 5/11/2021 using yfinance module and then place the data into the Kinesis Delivery Stream, stored the data in S3 bucket and then used AWS Glue to crawl the data in the S3 bucket. Then used Athena to gain insight into our streamed data.

Here is a diagram of how data flows in this project

![](C:\Users\winny\Downloads\STA9760F2020_ Project 3 Diagram.jpg)



#### Kinesis Configurations

<img src='assets\kinesis_config.png'>





#### Query used to retrieve highest hourly stock “high” per company

`with f2 as (select name,substring(ts,11,3) as hour,ts,high,max(high) over (partition by name,substring(ts,11,3)) as max_high from "finance-data"."sta9760glue22")
select name,ts,high,hour from f2 where high=max_high order by name,hour,ts`





