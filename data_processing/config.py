KAFKA = {
    "topic" : {
        "rcas_twitter_raw" : "rcas_twitter_raw",
        "rcas_twitter_after_sentiment" : "rcas_twitter_after_sentiment",
        "rcas_reddit_raw" : "rcas_reddit_raw",
        "rcas_reddit_after_sentiment" : "rcas_reddit_after_sentiment"
    },

    "bootstrap_servers" : ['106.52.240.156:19092'],
}

MLSERVICE = {
    "host" : "rcas_nginx",
    "port" : "8080"
}

