# Title
Real-time Cryptocurrency Analysis System

# Contacts
Liang, Zhihao  kelliang@connect.hku.hk
Wang, Xue

# Outline
* Abstract
* Introduction
* Background
* Related Works
* System Architecture
* Experimental Evaluation
* Discussion
* Conclusion
* References

# Abstract
Since the creation of Bitcoin, cryptocurrencies are attracting significant attentions from researchers. They have been proposing many solutions for analysing the price trend. One dimension of these researches is to analyse the sentiment trend in social media like Twitter and Reddit. Some of these solutions even implement near real-time processing on Spark framework. However Spark is a framework dedicated for batch processing, which suffers from high latency. To minimize latency, Spark has implemented streaming API by applying micro-batch processing. But its performance in iterative or interactive applications is still unsatisfactory. In the area of capital market, the price fluctuation is very fast. Analytics and stakeholders are demanding a timely system that can assist their decision making. In this background, the demand for a truely real-time crypotocurrency analysation platform is rising rapidly. In this paper, we propose a Flink-based cryptocurrency analysation system that can handle massive amount of data in real-time. Streaming data is evaluated continuously and the result is updated in seconds, not days or months.

# Introduction
* Introduction of cryptocurrency
* Introduction of social media(twitter, reddit)
* Significance of the paper
* technologies that we used, pros including fault tolerent, scalability, critical experiment result

Cryptocurrency is a kind of digital asset that's decentralized and secured by strong crypotography algorithms. Satoshi Nakamoto created the first generation cryptocurrency: Bitcoin in 2009. The validity of Bitcoin is provided by blockchain technology. A blockchain is a continuously growing list of records which is linked by hash function. Hash function ensures that non of the records can be modified without being caught by others. Since 2009, many other altcoins have been created. There are over 5000 altcoins in the cryptocurrency market till May 2020<ref>https://news.bitcoin.com/altcoins-why-over-5000/</ref>. The most famous altcoins include Ripple, Litecoin, Monero and more are created as a substitution for Bitcoin. These altcoins claim to offer better anonymity and faster transaction confirmation. However Bitcoin still take the lion share of the crypto market. On May 13, 2020, Bitcoin dominant 67.2% of the crypto market at the price $8893. Crypto market is highly fluctuated, over 30% of price fluctuation happens every day. So, investors need a timely price prediction system that can assit their decision making. 

<todo>introduce some real-time attempts of cryptocurrency analysis</todo>

The Efficient Market Hypothesis states that current stock prices have reflected all the available information. And price variation is largely driven by incoming information. These new information broadcasts on social media like twitter and reddit rappidly. Researchers have devoted to find the correlation between public mood and stock price. One approach is to do sentiment analysis on tweets by applying machine learning algorithms. 

<todo>which is the first paper that do sentiment on social media to predict cryptocurrency price</todo>

<todo>arrangement for the rest of the paper</todo>
The rest of paper is structured as follows.
<todo>introduce each setion</todo>


# Background（凑字数的)
<todo>* History of big data</todo>

## Traditional ETL and Business Intelligence
For many years, ETL (Extract, Transform and Load) is the mainstrem procedure for business intelligence and data analysis. The objective of ETL is to extract data from source system, apply some transformation, and finally load into target data store. However traditional ETL systems are limited by their scalability and fault tolerent ability. According to a report presented in 2017 by IDC<ref>https://www.seagate.com/files/www-content/our-story/trends/files/idc-seagate-dataage-whitepaper.pdf</ref>the global data volume will grow expronentially from 33 zettabytes in 2018 to 175 zettabytes by 2025. IDC also forecasts that we will have 150 billions devices connected globally by 2025. And real-time data will account for around 30 percents of the global data. Traditional ETL can't process this huge volume of data in acceptable time. We demand for a system that's able to distribute computations to thousands of machines and runs parallely.

## MapReduce
<ref>https://dl.gi.de/bitstream/handle/20.500.12116/20456/327.pdf?sequence=1</ref>
<ref>https://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html</ref>

<ref>who proposed mapreduce</ref>MapReduce is a programming model that is able to process vast amounts of datasets in parallel. It's inspired by the map and reduce operation in functional languages like Lisp. MapReduce is compose of three core operations: map, shuffle and reduce. A job is usually splited into multiple independent subtasks and run parallely on the map stage. Then the outputed data from map stage is shuffled by its key, so that data with the same key occurence on the same workder node. Finally, reducers start processing each group of data in parellel. MapReduce is a highly scalable programming model that can distribute data and computation to thousands of commodity machines. It uses re-execution as a mechanism for providing fault tolerance. To take the advantage of locality, MapReduce schedule map tasks to machines that are near to the input data. This is opposite to traditional ETL, which pulls all needed data from data warehouse to the execution machine. MapReduce makes the decision based on the fact that data size is usually far more larger than map tasks code size.

## Hadoop
Hadoop is a big data processing framwork inspired by GFS and MapReduce. It can scale out computation to many commodity machines. Hadoop is compose of Hadoop Distributed File System(HDFS) and Hadoop MapReduce. Both of the two components employ the master slave architecture. HDFS is a distributed file system that can manage large volume of data. It's an open source version of GFS. HDFS consist of a namenode and multiple datanodes. The namenode stores metadata of the distributed file system, including permissions, disk quota, access time etc. To read or write a file, HDFS clients must consult the namenode first. The namenode returns location awared metadata about where to read or write a file. Datanodes are where data actually stored. They register to the namenode and periodicly send heartbeats and block reports to the namenode. Block reports contain information of the blocks that datanode possesses. Hadoop MapReduce is a programming model for large scale data processing. Jobs are submmited through the jobtracker which is the master. The jobtracker keeps track of all MapReduce jobs and assign map or reduce tasks to tasktrackers. Tasktrackers are slave nodes which execute map or reduce tasks. The jobtracker monitor status of tasktrackers through heartbeats sent by tasktrackers. If a tasktracker is down, the jobtracker will reschedule those tasks to other tasktrackers.
<ref>http://www.alexanderpokluda.ca/coursework/cs848/CS848%20Paper%20Presentation%20-%20Alexander%20Pokluda.pdf</ref>

## Kappa architecture and Lambda Architecture
To accomodate the need for both high throughput and low latency, <ref>(N. Marz and J. Warren. Big data: principles and best practices of scalable realtime data systems. Manning, 2013.)</ref> proposed a mixed architecture: lambda architecture. Lambda architecture is a data processing paradigm that is capable of dealing with massive amount of data. It mixes both batch and stream processing methods. Lambda architecture is compose of batch layer and speed layer. The batch layer is focus on increasing the accuracy by taking account into all available data. The result produced by batch layer is equivalent to equation "query result = f(all data)". Where f is the processing logic for the data. The speed layer is focus on providing immediate view to the new incoming data. Query from clients are answered through the serving layer, which merges result from both batch layer and speed layer.

<todo>![lambda architecture](fig/ref_lambda_arch.png)</todo>

Kappa architecture is a simplified architecture with batch processing system removed. <ref>It's proposed by Jay Kreps https://www.oreilly.com/radar/questioning-the-lambda-architecture/</ref>It enable analytics to do data processing with a single technology stack. In kappa system, streaming data is processed in the speed layer and pushed to serving layer directly. Unlike lambda architecture, you don't have to maintain two set of code for batch layer and speed layer seperately.

<todo>![kappa architecture](fig/ref_kappa_arch.png)</todo>

## Spark
Hadoop has been a successful big data processing framework for years before the come up of spark. Spark is a cluster big data framework that supports in-memory computing. <todo>which paper propose spark, and what problem does it solve</todo> The main contribution of spark is that it introuduce the RDD data model into big data analysis area. This increase efficiency in processing interactive and iterative jobs. Hadoop MapReduce is not designed to reuse imtermidiate results. To reuse these results, we have to save them back to HDFS and reload them into memory at next iteration of MapReduce. This incurs performance penalty due to disk IO.  Spark minimizes the overhead by introducing in the resilient distributed datasets (RDD). A RDD is a collection of read only records that are partitioned across many machines. A RDD is created from external storage or other RDDs by the transformation operation. It can be explicitly cached in memory for resuse by multiple MapReduce tasks. To reuse a RDD in the future, users can persistent it to external storage. Fault tolerance of RDD is achieved by recording the lineage of the RDD. Lineages include information about how the RDD is drived from other RDDs. A RDD can be rebuilt if it's lost or crushed. <todo>Spark’s architecture consists of a Driver Program, a Cluster Manager and Worker Nodes</todo> <todo>spark stream and micro-batch streaming</todo>

## Flink
Apache flink is a distributed stateful stream processing framework. Flink is based on kappa architecture which unifies stream and batch data processing. <ref>Giselle van Dongen and Dirk Van den Poel benchmarks flink and spark streaming.</ref> The benchmark shows that flink outform spark streaming in two aspect. One is that flink processes streaming data with the lowest latency. The other is that flink provides better balance between latency and throughput. Because it supports more flexible windowing and time semantics. Flink employ the master slave structure, where jobmanager is the master and taskmanagers are the slaves. Jobmanager is responsible for scheduling tasks and coordinating checkpoints and recovery. Taskmanagers consist multiple task slots, which can execute task operators. Taskmanagers periodically report their status to the jobmanager by sending heartbeats.

There are five basic building blocks that compose flink: stream, state, time, window and checkpoint. Streams can be bounded or unbounded. Unbounded streams are streams never ended, while bounded streams are fix-sized datasets. Flink provides a DataStream API for unbounded stream and a DataSet API for bounded stream. Flink supports flexible window mechanism for the DataStream API, including time window and count window. A window declaration consist of three functions: a window assigner, a trigger and an evictor.  The window assigner assigns incoming data to windows. The trigger dertermines when the process function of the window start excuting. The evictor removes some data out of the window according to provided criteria. Time management is also critical for stream processing. Flink offers flexible notion of time: event time, ingestion time and processing time. 

Transformation operators can keep states like counter, machine learning model or intermediate aggregation result. States are key-value store embeded in stateful operators. Since states can be accessed locally, flink applications achieve high throughput and low latency. Flink offers exactly-once state consistency by regularly checkpointing operator states to external storage. Flink employs light weight Chandy-Lamport algorithm for asynchronous distributed checkpointing. The algorithm allows checkpointing without halting the execution of tasks. So, checkpoint and normal task execution can run in parallel.

<ref>https://flink.apache.org/flink-applications.html</ref>

# Related Works

# System Architecture
Rcas is a system aims at providing cryptocurrency investors some insights with the help of sentiment analysis. The analysis starts by collecting comment messages from social media. We extract those fields that we concern and filter out the others. Then, these preprocessed data are fed into our sentiment analysis model and produce some sentiment statistics. The next step is to aggregate these sentiment analysis and display it on dashboard. 
![rcas system architecture](fig/RCAS.png)
The overall architecture of RCAS system is shown in Figure 1. The system consist of five subsystems. (1) a streaming data source that collect data from Twitter streaming API; (2) a streaming message queue that stores and distribute data collected from data source; (3) a machine learning service that provides sentiment analysis services; (4) a streaming data analysis subsystem that can analyse data in distributed cluster; (5) a visualization module for displaying results. Our system runs and benchmarks on public cloud. To enable fast deployment, each of the components is run as docker container. In the following sections, we will introduce these subsystems one by one.

## Streaming Data Source
Streaming data source is a submodule that can streamingly push data into our system. It collects cryptocurrency related data from social media or any other channel. And performs some filtering that removes corrupted data. Then publishes them to the streaming message queue. Any social media platform are fine, such as twitter, reddit and facbook etc. The only difference is that the more diversify demogrphics is the platform the better result we will get.

## Streaming Message Queue
Streaming message queue is one of the core building blocks of the system. It plays as a message broker that collect and distribute immediate results. All of the data collected from data source phase are pushed to the streaming message queue. The message queue is a kafka cluster composed by multiple brokers.

There are many alternative databases or file systems like HDFS/MySQL for storing collected data. However, these storage alternatives are more suitable for batch processing than streaming processing. We prefer kafka for two reasons: First, we really don't care about data lost. According to the official statistics from twitter, the number of tweets sent per day is over 500 million.<ref>https://business.twitter.com/</ref> Loosing some of the messages will not affect our analysis much. So, at-most-once delivery semantics is sufficient for our case. Second, we really care about throughput and latency. Because cryptocurrecy market vary every seconds. MySQL is a traditional database that provides a rich set of transactionl operations. However, it's not suitable for storing large volume of data. Because it's not designed as a distributed database, and its throughput is limitted by a single machine. HDFS is a distributed file system that can provide high throughput. Multiple data blocks of the same file can be read from multiple data nodes parallelly. The blocks size of HDFS is usually larger than 64MB. This minimizes seek time of disk read head, and increase throughput. But the latency of HDFS is still at high level since it need to load data from disk for each read. 

Kafka is a better choice that provides both high throughput and low latency. Kafka is an open sourced distributed messaging system for dealing with logs. In kafka, a stream of messages is called a topic. Message producers can publish new messages to the topic. And message consumers can pull messages from a perticular topic. To maximize throughput, a topic is usually decomposed into multiple disjointed partitions. Thesee partitions are distributed among brokers that form the cluster. With this horizontally scalable architecture, multiple producers and consumers can operate on the same topic at the same time. Additionally, kafka increase throughput by batching messages and sending asynchrounously. Batching messages amortize network traffic overhead like connection establishment. Sending messages asynchrounously could saturate network capacity instead of blocking by receivers. Kafka reduce latency by relying on page cache and zero-copy. In a typical publish-subscribe system, consumers is usually lagging producers a little bit. At this case, consumers read data from page cache directly without having to access disks. 

<todo>ActiveMQ、RabbitMQ、Kafka、RocketMQ、ZeroMQ As a log based messaging system, kafka is able to retain data for a period of time.</todo>

## Machine Learning Services

## Real-Time Data Analysis
Data processed by ML service is then ready for aggregation analysis. The framework that we used for this phase is apache flink. In previous sections, we have introduced some background of flink, including its basic building blocks and architectures. Flink has been widely accepted in applications like fraud detection, anomaly detection and business event monitoring. It can handle both batch data and streaming data with the same underlying runtime environment. And provides flexible API for controling window, time and checkpointing. Spark is a direct competitor of flink in stream processing area. Comparing to spark streaming, flink offers more fine-grained control for windowing incoming data. In spark streaming, data are min-batched in processing time, and there is no option for batching in event-time. In the mean time, caculation of spark streaming is triggered globaly instead of operator by operator. While in flink, we can batch data in event time by specifying window assigner, and trigger caculation for each operator by setting its own trigger. <todo>in our system, why using flink is better</todo> In addition, flink provides lower latency than spark streaming, which is critical to our system. Our goal is to provide users with a system that can reveal the trend of cryptocurrencies in real-time. Flink can process incoming data in elementwise basis. While in spark streaming, it has to wait enough of data that can form a mini-batch, which increases latency. With the considerations above, we decided to use flink instead of spark streaming. 
<todo>make a table comparison among flink, storm, spark, spark streaming</todo>

## Visualization
Aggregated result from flink is then published to external data store for visualization. The data store we use is redis, an in-memory data storage server. The output of our system includes a word count set and a tuple with 3 elements. Typically, the word count set contains only thousands of records, since the number of vocabulary in common use is just 3000. We need to update the word count set frequently. So, we need a data store that supports fast update. Redis and memcached are potential candidates for the task. Memcached is a simple key-value in-memory store for small chunk objects. It's usually used as a distributed share memory and caching server. But memcached only support string data type. If you want some advanced functionalities, you must implement them by youself. Redis is a powerful key-value data structure server. It preserves data in main memory for later fast retrieval. By the way, redis also supports persistence of data in the form of binary(RDB) or append only log(AOF). When redis server is crushed, it can recover from latest RDB or AOF file. Redis supports multiple data types, including string, list, map, set, sorted set, bitmap and more. The speed of both memcached and redis are extremely fast, they can handle more than 100000 requests per second at a single node. Considering the flexibilites that redis offers, we decide to use redis as our result data store. In our case, we use sorted set and string data type. String is for storing some running statistics and sorted set is for storing analysed results. We have a dashboard for displaying these results as well.

# Experimental Evaluation
We conduct experimental evaluation in tencent cloud.

## Streaming Data Collection
<ref>https://developer.twitter.com/en/docs/tweets/filter-realtime/api-reference/post-statuses-filter</ref>
We collect real-time data from the twitter API. There are many other media platforms for data collection, like facebook, reddit etc. We choose twitter for the reason that it has the most largest and diversified population of users. As of Sep 2019, the number of daily active users in twitter is 152 million. International users makes up around 79% of the total users of twitter. <ref>https://www.omnicoreagency.com/twitter-statistics/#:~:text=Twitter%20Demographics&text=There%20are%20262%20million%20International,are%20on%20the%20platform%20daily.</ref> Twitter provide a streaming API that returns tweets containing a set of keywords. The keywords we uses include #croptocurrency, #bitcoin and #ethereum etc. However there is rate limit for free API users. We can only initiate no more than 450 requests in 15 minutes window. To address this issue, we collect data in advance. We use the tweepy:3.8.0 library for developing the streaming data source module. Tweepy is a python library that wraps many functionalities of twitter streaming API. It enables fast development of twitter applications.

<todo>how many data did we collect</todo>
For each tweet, we extract information like tweet ID, create time, quote count, reply count, retweet count, favorite count, language, comment text. For the reason that our sentiment analysis model can only handle english sentences, tweets written in language other than english are filtered out. Other unusual characters, emojis are also removed.

## Kafka Cluster
In our system, we have 16 kafka broker. They are running on the same machine with 16 CPU cores, each topic are decomposed into 16 partitions. For each partition, there exists only one replica. Because data reliability is insignificant for our system. We have created two topics: one for collecting data from twitter streaming API, the other is for storing messages which has been processed by our machine learning service. The configurations of kafka cluster machine are shown below:

<todo>should in table form</todo>
Components    Specifications
-------------------------
Model         IT3.4XLARGE64
CPU           Intel Xeon Skylake 6133(2.5 GHz)
#vCores       16
RAM           64GB
Network       6Gbps
OS            Ubuntu:4.15.0-54-generic
Hard Disk     1×3720GB NVMe SSD

## Sentiment Analysis

## Data Aggregation
Data returned from sentiment analysis include the following fields:

<todo>should in table form</todo>
Fields                Descriptions
-------------------------------------------------
id_str                ID of this message
created_at            Creation time of the message
quote_count           Number of quotes by other users
reply_count           Number of reply by other users
retweet_count         Number of retweets byt other users
favorite_count        Count of favorite
geo                   Geology location
coordinates           GPS coordination
timestamp_ms          Timestamp of this message
lang                  Language
text                  Text body (user comments)
sentiment_neg         Sentiment result, negative value
sentiment_neu         Sentiment result, neutral value
sentiment_pos         Sentiment result, positive value
sentiment_compound    Sentiment result, compound value

In particular, the three sentiment_xxx fields represent the weight of negative mood, neutral mood and positive mood correspondingly. Where sentiment_neg + sentiment_neu + sentiment_pos = 1.Our system presents two indicators of cryptocurrency price trend. One is a word cloud chart presenting 30 of the most commonly used words in user comments. The other is the percentage of negative, neutral and positive opinion in 3 minutes window. In order to measure the performance of the system, we also return the number of messages that have been processed, and duration since the bootstrap of the system.

### Word Cloud of Twitter User Comments
Word cloud is a chart that users can quickly perceive the most prominent term on it. The higher weight is a term, the large font size it has on the chart. To produce a word cloud we must supply a weighted list of words. The list is in word-count pair form. Here is a sample list:

Words         Count
-------------------------
bitcoin       39882
good          28933
rise          18839
promotion     16893
eth           12898
...

As is shown on the sample weighted list, bitcoin is the most frequently mentioned word with the count 39882. We conduct calculation by extracting user comments from each tweet first. <todo>may be we can do word selection here</todo> Then we split these comments into words and aggregate the count. Finally, the results are written to redis as a sorted set where score is the count of words. Our visualization subsystem extract the top 30 words by score and construct a word cloud for displaying. The word cloud of top 30 most common words is a good indicator that reveals the trend of user opinion. It displays the hot topic at the time, which gives investors some sense of what's going on in the market.

### Opinion Variation
We have done sentiment analysis for user comments in the machine learning subsystem. At this step, we would like to see the variation of user opinion in time. Thus, we evaluate the proportion of different user opinion every 3 minutes. The result is written to redis as a sorted set with a timestamp as the score. A stepped area chart is used for displaying 20 of the most recent records. <todo>Figurexxx shows an example result</todo>

## Performance


Components    Specifications
-------------------------
Model         CN3.2XLARGE16
CPU           Intel Xeon Skylake 6146(3.2 GHz)
#vCores       8
RAM           16GB
Network       6Gbps
OS            Ubuntu:4.15.0-54-generic
Hard Disk     1×50GB


# Discussion

# Conclusion

# References