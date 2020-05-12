package ink.kelvin;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.functions.ReduceFunction;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.shaded.jackson2.com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.AllWindowedStream;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.util.serialization.JSONKeyValueDeserializationSchema;
import org.apache.flink.util.Collector;

import java.util.Properties;

public class RcasStreamJob {

    public static void main(String[] args) throws Exception {

        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);

        DataStream<ObjectNode> kafkaStream = makeKafkaStream(env);

        DataStream<Tweet> tweetStream = kafkaStream
                .map(new ExtractTweet());

        AnalyTweetWindowNegNeuPos(tweetStream).print();

//      tweetStream.map(new TweetToString()).print();
        env.execute("RCAS Analysis Start!");
    }

    public static DataStream<Tuple3<Double, Double, Double>> AnalyTweetWindowNegNeuPos(DataStream<Tweet> teetStream){
        DataStream<Tuple3<Double, Double, Double>> nnpStream = teetStream.flatMap(
                new FlatMapFunction<Tweet, Tuple3<Double, Double, Double>>() {
                    @Override
                    public void flatMap(Tweet tweet, Collector<Tuple3<Double, Double, Double>> collector) throws Exception {
                        Tuple3<Double, Double, Double> t = new Tuple3<Double, Double, Double>(tweet.sentiment_neg, tweet.sentiment_neu, tweet.sentiment_pos);
                        collector.collect(t);
                    }
                })
                .windowAll(TumblingProcessingTimeWindows.of(Time.seconds(5)))
                .reduce(new ReduceFunction<Tuple3<Double, Double, Double>>() {
                    @Override
                    public Tuple3<Double, Double, Double> reduce(Tuple3<Double, Double, Double> t1, Tuple3<Double, Double, Double> t2) throws Exception {
                        Double sum = t1.f0 + t2.f0 + t1.f1 + t2.f1 + t1.f2 + t2.f2;
                        Tuple3<Double, Double, Double> t = new Tuple3<Double, Double, Double>((t1.f0+t2.f0)/sum , (t1.f1+t2.f1)/sum, (t1.f2+t2.f2)/sum);
                        return t;
                    }
                });
        return nnpStream;
    }

    private static DataStream<ObjectNode> makeKafkaStream(StreamExecutionEnvironment env) {
        Properties props = new Properties();
        props.setProperty("bootstrap.servers", "129.204.135.185:19092");
        props.setProperty("group.id", "flink");

        // More info about JSONKeyValueDeserializationSchema is on
        // https://ci.apache.org/projects/flink/flink-docs-release-1.9/api/java/org/apache/flink/streaming/util/serialization/JSONKeyValueDeserializationSchema.html
        FlinkKafkaConsumer<ObjectNode> kafkaConsumer = new FlinkKafkaConsumer<>(
                "rcas_twitter_after_sentiment", new JSONKeyValueDeserializationSchema(false), props);
        kafkaConsumer.setStartFromLatest();

        return env.addSource(kafkaConsumer);
    }


    public static class TweetToString implements MapFunction<Tweet, String>{
        @Override
        public String map(Tweet tweet) throws Exception {
            return tweet.toString();
        }
    }

    public static class RedditToString implements MapFunction<Reddit, String>{
        @Override
        public String map(Reddit reddit) throws Exception {
            return reddit.toString();
        }
    }

    public static class ExtractTweet implements MapFunction<ObjectNode, Tweet>{
        @Override
        public Tweet map(ObjectNode jsonNodes) throws Exception {
            ObjectNode value = (ObjectNode)jsonNodes.get("value");

            Tweet tweet = new Tweet();
            tweet.id_str = value.get("id_str").asText("");
            tweet.created_at = value.get("created_at").asText("");
            tweet.quote_count = value.get("quote_count").asInt(0);
            tweet.reply_count = value.get("reply_count").asInt(0);
            tweet.retweet_count = value.get("retweet_count").asInt(0);
            tweet.favorite_count = value.get("favorite_count").asInt(0);
            tweet.geo = value.get("geo").asText("");
            tweet.coordinates = value.get("coordinates").asText("");
            tweet.timestamp_ms = value.get("timestamp_ms").asText("");
            tweet.lang = value.get("lang").asText("");
            tweet.source = value.get("source").asText("");
            tweet.text = value.get("text").asText("");
            tweet.sentiment_neg = value.get("sentiment").get("neg").asDouble(0.0);
            tweet.sentiment_neu = value.get("sentiment").get("neu").asDouble(0.0);
            tweet.sentiment_pos = value.get("sentiment").get("pos").asDouble(0.0);
            tweet.sentiment_compound = value.get("sentiment").get("compound").asDouble(0.0);

            return tweet;
        }
    }

    public static class ExtractReddit implements MapFunction<ObjectNode, Reddit>{
        @Override
        public Reddit map(ObjectNode jsonNodes) throws Exception {
            ObjectNode value = (ObjectNode)jsonNodes.get("value");

            Reddit reddit = new Reddit();
            reddit.id = value.get("id").asText("");
            reddit.created_utc = value.get("created_utc").asText("");
            reddit.link_id = value.get("link_id").asText("");
            reddit.link_title = value.get("link_title").asText("");
            reddit.subreddit_id = value.get("subreddit_id").asText("");
            reddit.score = value.get("score").asDouble(0.0);
            reddit.stickied = value.get("stickied").asText("");
            reddit.likes = value.get("likes").asInt(0);
            reddit.permalink = value.get("permalink").asText("");
            reddit.text = value.get("text").asText("");
            reddit.sentiment_neg = value.get("sentiment").get("neg").asDouble(0.0);
            reddit.sentiment_neu = value.get("sentiment").get("neu").asDouble(0.0);
            reddit.sentiment_pos = value.get("sentiment").get("pos").asDouble(0.0);
            reddit.sentiment_compound = value.get("sentiment").get("compound").asDouble(0.0);

            return reddit;
        }
    }

    public static class Tweet{
        public String  id_str;
        public String  created_at;
        public Integer quote_count;
        public Integer reply_count;
        public Integer retweet_count;
        public Integer favorite_count;
        public String  geo;
        public String  coordinates;
        public String  timestamp_ms;
        public String  lang;
        public String  source;
        public String  text;
        public Double  sentiment_neg;
        public Double  sentiment_neu;
        public Double  sentiment_pos;
        public Double  sentiment_compound;

        public Tweet(){}
        public String toString(){
            return id_str + " " + created_at + " " + quote_count + " " + reply_count + " " + retweet_count + " " + favorite_count + " " +
                    geo + " " + coordinates + " " + timestamp_ms + " " + lang + " " + source + " " + text + " " +
                    sentiment_neg + " " + sentiment_neu + " " + sentiment_pos + " " + sentiment_compound;
        }
    }

    public static class Reddit{
        public String  id;
        public String  created_utc;
        public String  link_id;
        public String  link_title;
        public String  subreddit_id;
        public Double  score;
        public String  stickied;
        public Integer likes;
        public String  permalink;
        public String  text;
        public Double  sentiment_neg;
        public Double  sentiment_neu;
        public Double  sentiment_pos;
        public Double  sentiment_compound;

        public Reddit(){}
        public String toString(){
            return id + " " + created_utc + " " + link_id + " " + link_title + " " + subreddit_id + " " +
                    score + " " +stickied + " " + likes + " " + permalink + " " + text + " " +
                    sentiment_neg + " " + sentiment_neu + " " + sentiment_pos + " " + sentiment_compound;
        }
    }

}