# Outline

# Abstract
Since the creation of Bitcoin, cryptocurrencies are attracting significant attentions from researchers. They have been proposing many solutions for analysing the price trend. One dimension of these researches is to analyse the sentiment trend in social media like Twitter and Reddit. Some of these solutions even implement approximately real-time processing on Spark framework. However the data volume is increasing rapidly in recent years.

<todo>People are demanding a timely system that can help them to detect the fluctuation of cryptocurrency market.</todo>

The demand for a truely real-time crypotocurrency analysation platform is rising. In this paper, we propose a Flink-based cryptocurrency analysation system that can handle massive amount of data in real time. Streaming data is evaluated continuously and the result is updated to dashboard instantly. The system apply streaming f

<todo>technologies that we used, pros including fault tolerent, scalability, critical experiment result</todo>


# Introduction
* Introduction of cryptocurrency
* Introduction of social media(twitter, reddit)

Cryptocurrency is a kind of digital asset that's decentralized and secured by strong crypotography algorithms. Satoshi Nakamoto created the first generation cryptocurrency: Bitcoin in 2009. The validity of Bitcoin is provided by Blockchain technology. A blockchain is a continuously growing list of records which is linked by hash function. Hash function ensures that non of the records can be modified without being caught by other. 

<todo>altcoin, proof-of-work scheme, proof-of-stake scheme</todo>
Since 2009, many other altcoins have been created. 

<todo>crypto coin market, price, historycal high, current status, fluctuation</todo>


The Efficient Market Hypothesis states that current stock prices have reflected all the available information. And price variation is largely driven by incoming information. These new information broadcasts on social media like twitter and reddit rappidly. Researchers have devoted to find the correlation between public mood and stock price. One approach is to do sentiment analysis on tweets by applying machine learning algorithms. 

<todo>which is the first paper that do sentiment on social media to predict cryptocurrency price</todo>



# Background（凑字数的)
* History of big data
* Traditional business intelligence
* MapReduce
* Hadoop
* Kappa architecture and Lambda Architecture
* Spark
* Flink


<todo>Traditional business intelligence</todo>
For many years, ETL (Extract, Transform and Load) is the mainstrem procedure for business intelligence and data analysis. The first step is to extract data from multiple sources. The extracted data is then processed in the transform stage. Finally, these data are loaded to target data store.

<todo>MapReduce</todo>
<todo>Hadoop</todo>
<todo>Kappa architecture and Lambda Architecture</todo>
Lambda architecture is a data processing architure that is capable of dealing with massive amount of data. It mixes both batch and stream processing methods. Lambda architecture is compose of batch layer and speed layer. The batch layer is focus on increasing the accuracy by taking account into all available data. The speed layer is focus on providing immediate view to the new incoming data.

<todo>![lambda architecture](fig/ref_lambda_arch.png)</todo>

Kappa architecture is a simplified architecture with batch processing system removed. It enable analytics to do data processing with a single technology stack. 

<todo>![lambda architecture](fig/ref_kappa_arch.png)</todo>

<todo>Spark</todo>

<todo>Flink</todo>

Apache flink is a distributed stateful stream processing framework. 

Building blocks of flink:
<ref>https://flink.apache.org/flink-applications.html</ref>
* Stream: Bounded, unbounded
* State: 
* Time: Event-time, Ingestion time, Processing time


Characteristics of flink
* High throughput
* Low latency
* Exactly once semantcs
* Event Processing
* State management
* Time sementics
* Fault tolerent

<ref>Flink guarantees exactly-once state consistency in case of failures by periodically and asynchronously checkpointing the local state to durable storage.</ref>





# Related Works


# System Architecture


# Experimental Evaluation

# Discussion

# Conclusion

# References