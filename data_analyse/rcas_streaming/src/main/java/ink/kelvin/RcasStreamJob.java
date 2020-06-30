package ink.kelvin;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.functions.RichFlatMapFunction;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.tuple.Tuple4;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.shaded.jackson2.com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.AssignerWithPeriodicWatermarks;
import org.apache.flink.streaming.api.watermark.Watermark;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.redis.RedisSink;
import org.apache.flink.streaming.connectors.redis.common.config.FlinkJedisPoolConfig;
import org.apache.flink.streaming.connectors.redis.common.mapper.RedisCommand;
import org.apache.flink.streaming.connectors.redis.common.mapper.RedisCommandDescription;
import org.apache.flink.streaming.connectors.redis.common.mapper.RedisMapper;
import org.apache.flink.streaming.util.serialization.JSONKeyValueDeserializationSchema;
import org.apache.flink.util.Collector;

import javax.annotation.Nullable;
import java.time.Duration;
import java.time.Instant;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Properties;
import java.util.Set;
import java.util.regex.Pattern;

public class RcasStreamJob {
    // ##################### Configuration #####################
    static String bootstrapServer = "42.194.194.145:19092";
    static String kafkaTopic = "rcas_reddit_after_sentiment";
    static String kafkaGroupID = "flink";
    static String RedisHost = "106.52.252.27";
    // #########################################################

    private static DataStream<ObjectNode> makeKafkaStream(StreamExecutionEnvironment env) {
        Properties props = new Properties();
        props.setProperty("bootstrap.servers", bootstrapServer);
        props.setProperty("group.id", kafkaGroupID);

        FlinkKafkaConsumer<ObjectNode> kafkaConsumer = new FlinkKafkaConsumer<>(
                kafkaTopic, new JSONKeyValueDeserializationSchema(false), props);
        //kafkaConsumer.setStartFromLatest();
        return env.addSource(kafkaConsumer);
    }

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);
        //env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
        //env.enableCheckpointing(1000*60);
        //env.setParallelism(6);

        FlinkJedisPoolConfig redisConf = new FlinkJedisPoolConfig.Builder()
                .setHost(RedisHost)
                .setMaxTotal(128)
                .setTimeout(10*1000)
                .build();

        DataStream<ObjectNode> kafkaStream = makeKafkaStream(env);
        //DataStream<Tweet> tweetStream = kafkaStream.map(new ExtractTweet());
        DataStream<Reddit> radditStream = kafkaStream.map(new ExtractReddit());

//        AnalyTweetWindowNegNeuPos(tweetStream, 5).print();
//        AnalyTweetProcessStatistics(tweetStream).print();
//        AnalyTweetWordCloud(tweetStream).print();
//        AnalyTweetWindowNegNeuPos(tweetStream, 5).addSink(new RedisSink<>(redisConf, new WindowNegNeuPosRedisMapper()));
//        AnalyTweetProcessStatistics(tweetStream).addSink(new RedisSink<>(redisConf, new ProcessStatisticsRedisMapper()));
//        AnalyTweetWordCloud(tweetStream).addSink(new RedisSink<>(redisConf, new WordCloudRedisMapper()));

        AnalyRedditWindowNegNeuPos(radditStream, 100).print();
        AnalyRedditProcessStatistics(radditStream).print();
        AnalyRedditWordCloud(radditStream).print();

        AnalyRedditWindowNegNeuPos(radditStream, 100).addSink(new RedisSink<>(redisConf, new WindowNegNeuPosRedisMapper()));
        AnalyRedditProcessStatistics(radditStream).addSink(new RedisSink<>(redisConf, new ProcessStatisticsRedisMapper()));
        AnalyRedditWordCloud(radditStream).addSink(new RedisSink<>(redisConf, new WordCloudRedisMapper()));

        env.execute("RCAS Analysis");
    }

    public static DataStream<Tuple2<String, Integer>> AnalyRedditWordCloud(DataStream<Reddit> stream){
        return stream
                .map(t -> t.text)
                .flatMap(new Splitter())
                .filter(t -> wordFilterLogic(t.f0))
                .keyBy(0)
                .sum(1);
    }

    public static DataStream<Tuple2<Long, Long>> AnalyRedditProcessStatistics(DataStream<Reddit> stream){
        return stream.keyBy("nokey").flatMap(new RedditCountAndDuration());
    }

    public static DataStream<Tuple4<String, Double, Double, Double>> AnalyRedditWindowNegNeuPos(DataStream<Reddit> stream, Integer count){
        return stream
                .filter(t -> t.created_utc.matches("^[0-9]*$"))
                .flatMap(new FlatMapFunction<Reddit, Tuple4<String, Double, Double, Double>>() {
                    @Override
                    public void flatMap(Reddit reddit, Collector<Tuple4<String, Double, Double, Double>> collector) throws Exception {
                        Tuple4<String, Double, Double, Double> t = new Tuple4<String, Double, Double, Double>(reddit.created_utc, reddit.sentiment_neg, reddit.sentiment_neu, reddit.sentiment_pos);
                        collector.collect(t);
                    }})
                .countWindowAll(count)
                .reduce((t1, t2) -> new Tuple4<>(t2.f0, (t1.f1*0.95 + t2.f1*0.05) , (t1.f2*0.95 + t2.f2*0.05), (t1.f3*0.95 + t2.f3*0.05)))
                .map(new MapFunction<Tuple4<String, Double, Double, Double>, Tuple4<String, Double, Double, Double>>() {
                    @Override
                    public Tuple4<String, Double, Double, Double> map(Tuple4<String, Double, Double, Double> t) throws Exception {
                        Double sum = t.f1 + t.f2 + t.f3;
                        return new Tuple4<>(t.f0, t.f1 / sum, t.f2 / sum, t.f3 / sum);
                    }
                });
    }

    public static DataStream<Tuple2<String, Integer>> AnalyTweetWordCloud(DataStream<Tweet> tweetStream){
        return tweetStream.filter(t -> t.lang.equals("en"))
                .map(t -> t.text)
                .flatMap(new Splitter())
                .filter(t -> wordFilterLogic(t.f0))
                .keyBy(0)
                .sum(1);
    }

    public static DataStream<Tuple2<Long, Long>> AnalyTweetProcessStatistics(DataStream<Tweet> tweetStream){
        return tweetStream.keyBy("geo").flatMap(new TweetCountAndDuration());
    }

    public static DataStream<Tuple4<String, Double, Double, Double>> AnalyTweetWindowNegNeuPos(DataStream<Tweet> tweetStream, Integer seconds){
        return tweetStream
                .filter(t -> t.lang.equals("en"))
                .flatMap(new FlatMapFunction<Tweet, Tuple4<String, Double, Double, Double>>() {
                    @Override
                    public void flatMap(Tweet tweet, Collector<Tuple4<String, Double, Double, Double>> collector) throws Exception {
                        Tuple4<String, Double, Double, Double> t = new Tuple4<String, Double, Double, Double>(String.valueOf(Instant.now().getEpochSecond()), tweet.sentiment_neg, tweet.sentiment_neu, tweet.sentiment_pos);
                        collector.collect(t);
                    }})
                .windowAll(TumblingProcessingTimeWindows.of(Time.seconds(seconds)))
                .reduce((t1, t2) -> new Tuple4<>(t2.f0, (t1.f1*0.95 + t2.f1*0.05) , (t1.f2*0.95 + t2.f2*0.05), (t1.f3*0.95 + t2.f3*0.05)))
                .map(new MapFunction<Tuple4<String, Double, Double, Double>, Tuple4<String, Double, Double, Double>>() {
                    @Override
                    public Tuple4<String, Double, Double, Double> map(Tuple4<String, Double, Double, Double> t) throws Exception {
                        Double sum = t.f1 + t.f2 + t.f3;
                        return new Tuple4<>(t.f0, t.f1 / sum, t.f2 / sum, t.f3 / sum);
                    }
                });
    }

    public static class ProcessStatisticsRedisMapper implements RedisMapper<Tuple2<Long, Long>> {
        @Override
        public RedisCommandDescription getCommandDescription() {
            return new RedisCommandDescription(RedisCommand.SET);
        }

        @Override
        public String getKeyFromData(Tuple2<Long, Long> data) {
            return "ps";
        }

        @Override
        public String getValueFromData(Tuple2<Long, Long> data) {
            return data.f0.toString() + " " + data.f1.toString();
        }

    }

    public static class WindowNegNeuPosRedisMapper implements RedisMapper<Tuple4<String, Double, Double, Double>> {
        @Override
        public RedisCommandDescription getCommandDescription() {
            return new RedisCommandDescription(RedisCommand.ZADD, "nnp");
        }

        @Override
        public String getKeyFromData(Tuple4<String, Double, Double, Double> data) {
            return data.f1.toString() + " " + data.f2.toString() + " " + data.f3.toString();
        }

        @Override
        public String getValueFromData(Tuple4<String, Double, Double, Double> data) {
            return data.f0;
        }
    }

    public static class WordCloudRedisMapper implements RedisMapper<Tuple2<String, Integer>> {
        @Override
        public RedisCommandDescription getCommandDescription() {
            return new RedisCommandDescription(RedisCommand.ZADD, "word_cloud");
        }
        @Override
        public String getKeyFromData(Tuple2<String, Integer> data) {
            return data.f0;
        }
        @Override
        public String getValueFromData(Tuple2<String, Integer> data) {
            return data.f1.toString();
        }
    }

    public static class Splitter implements FlatMapFunction<String, Tuple2<String, Integer>> {
        @Override
        public void flatMap(String sentence, Collector<Tuple2<String, Integer>> out) throws Exception {
            for (String word: sentence.split(" ")) {
                out.collect(new Tuple2<String, Integer>(word.toLowerCase(), 1));
            }
        }
    }

    public static Boolean wordFilterLogic(String word){
        Boolean retain = true;

        // Only retain words with no punctuation and strange characters
        if(!Pattern.matches("[a-zA-Z]*", word)){
            retain = false;
        }

        // Remove stop words
        Set<String> hashSet = new HashSet<String>();
        hashSet.addAll(Arrays.asList("because", "people","will", " ", "", "0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "A", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "after", "afterwards", "ag", "again", "against", "ah", "ain", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appreciate", "approximately", "ar", "are", "aren", "arent", "arise", "around", "as", "aside", "ask", "asking", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "B", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "been", "before", "beforehand", "beginnings", "behind", "below", "beside", "besides", "best", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "C", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "ci", "cit", "cj", "cl", "clearly", "cm", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "could", "couldn", "couldnt", "course", "cp", "cq", "cr", "cry", "cs", "ct", "cu", "cv", "cx", "cy", "cz", "d", "D", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "dj", "dk", "dl", "do", "does", "doesn", "doing", "don", "done", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "E", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "F", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "G", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "H", "h2", "h3", "had", "hadn", "happens", "hardly", "has", "hasn", "hasnt", "have", "haven", "having", "he", "hed", "hello", "help", "hence", "here", "hereafter", "hereby", "herein", "heres", "hereupon", "hes", "hh", "hi", "hid", "hither", "hj", "ho", "hopefully", "how", "howbeit", "however", "hr", "hs", "http", "hu", "hundred", "hy", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "im", "immediately", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "inward", "io", "ip", "iq", "ir", "is", "isn", "it", "itd", "its", "iv", "ix", "iy", "iz", "j", "J", "jj", "jr", "js", "jt", "ju", "just", "k", "K", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "ko", "l", "L", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "M", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "my", "n", "N", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "neither", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "O", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "otherwise", "ou", "ought", "our", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "P", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "pp", "pq", "pr", "predominantly", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "Q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "R", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "S", "s2", "sa", "said", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "seem", "seemed", "seeming", "seems", "seen", "sent", "seven", "several", "sf", "shall", "shan", "shed", "shes", "show", "showed", "shown", "showns", "shows", "si", "side", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somehow", "somethan", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "sz", "t", "T", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "thats", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "thereof", "therere", "theres", "thereto", "thereupon", "these", "they", "theyd", "theyre", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "U", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "used", "useful", "usefully", "usefulness", "using", "usually", "ut", "v", "V", "va", "various", "vd", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "W", "wa", "was", "wasn", "wasnt", "way", "we", "wed", "welcome", "well", "well-b", "went", "were", "weren", "werent", "what", "whatever", "whats", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "whom", "whomever", "whos", "whose", "why", "wi", "widely", "with", "within", "without", "wo", "won", "wonder", "wont", "would", "wouldn", "wouldnt", "www", "x", "X", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "Y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "your", "youre", "yours", "yr", "ys", "yt", "z", "Z", "zero", "zi", "zz"));
        hashSet.addAll(Arrays.asList("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"));

        if(hashSet.contains(word)){
            retain = false;
        }

        return retain;
    }

    public static class TweetCountAndDuration extends RichFlatMapFunction<Tweet, Tuple2<Long, Long>> {
        private transient ValueState<Tuple2<Long, Instant>> state;

        @Override
        public void flatMap(Tweet input, Collector<Tuple2<Long, Long>> out) throws Exception {
            Tuple2<Long, Instant> stateValue = state.value();

            stateValue.f0 += 1;
            Duration duration = Duration.between(stateValue.f1, Instant.now());
            state.update(stateValue);

            out.collect(new Tuple2<Long, Long>(stateValue.f0, duration.toNanos()/1000000000));
        }

        @Override
        public void open(Configuration config) {
            ValueStateDescriptor<Tuple2<Long, Instant>> descriptor =
                    new ValueStateDescriptor<>(
                            "processing_statistics", // the state name
                            TypeInformation.of(new TypeHint<Tuple2<Long, Instant>>() {}), // type information
                            Tuple2.of(0L, Instant.now())); // default value of the state, if nothing was set
            state = getRuntimeContext().getState(descriptor);
        }
    }

    public static class RedditCountAndDuration extends RichFlatMapFunction<Reddit, Tuple2<Long, Long>> {
        private transient ValueState<Tuple2<Long, Instant>> state;

        @Override
        public void flatMap(Reddit input, Collector<Tuple2<Long, Long>> out) throws Exception {
            Tuple2<Long, Instant> stateValue = state.value();

            stateValue.f0 += 1;
            Duration duration = Duration.between(stateValue.f1, Instant.now());
            state.update(stateValue);

            out.collect(new Tuple2<Long, Long>(stateValue.f0, duration.toNanos()/1000000000));
        }

        @Override
        public void open(Configuration config) {
            ValueStateDescriptor<Tuple2<Long, Instant>> descriptor =
                    new ValueStateDescriptor<>(
                            "processing_statistics", // the state name
                            TypeInformation.of(new TypeHint<Tuple2<Long, Instant>>() {}), // type information
                            Tuple2.of(0L, Instant.now())); // default value of the state, if nothing was set
            state = getRuntimeContext().getState(descriptor);
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
            reddit.subreddit_id = value.get("subreddit_id").asText("");
            reddit.score = value.get("score").asDouble(0.0);
            reddit.stickied = value.get("stickied").asText("");
            reddit.text = value.get("body").asText("");
            reddit.sentiment_neg = value.get("sentiment").get("neg").asDouble(0.0);
            reddit.sentiment_neu = value.get("sentiment").get("neu").asDouble(0.0);
            reddit.sentiment_pos = value.get("sentiment").get("pos").asDouble(0.0);
            reddit.sentiment_compound = value.get("sentiment").get("compound").asDouble(0.0);
            reddit.nokey = "nokey";

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
        public String  text;
        public Double  sentiment_neg;
        public Double  sentiment_neu;
        public Double  sentiment_pos;
        public Double  sentiment_compound;

        public Tweet(){}
        public String toString(){
            return id_str + " " + created_at + " " + quote_count + " " + reply_count + " " + retweet_count + " " + favorite_count + " " +
                    geo + " " + coordinates + " " + timestamp_ms + " " + lang  + " " + text + " " +
                    sentiment_neg + " " + sentiment_neu + " " + sentiment_pos + " " + sentiment_compound;
        }
    }

    public static class Reddit{
        public String  id;
        public String  created_utc;
        public String  link_id;
        public String  subreddit_id;
        public Double  score;
        public String  stickied;
        public String  text;
        public Double  sentiment_neg;
        public Double  sentiment_neu;
        public Double  sentiment_pos;
        public Double  sentiment_compound;
        public String  nokey = "nokey";

        public Reddit(){}
        public String toString(){
            return id + " " + created_utc + " " + link_id + " " + subreddit_id + " " +
                    score + " " +stickied  + " " + text + " " +
                    sentiment_neg + " " + sentiment_neu + " " + sentiment_pos + " " + sentiment_compound;
        }

        // More info about JSONKeyValueDeserializationSchema is on
        // https://ci.apache.org/projects/flink/flink-docs-release-1.9/api/java/org/apache/flink/streaming/util/serialization/JSONKeyValueDeserializationSchema.html
    }
}