import redis

##################### Configuration #####################
red = redis.Redis(host='localhost', port=6379, db=0)
redis_wc = 'word_cloud'
redis_nnp = 'nnp'
redis_ps = 'ps'
##################### Configuration #####################

# def get_nnp(num):
#     nnp = red.zrevrange(name=redis_nnp, start=0, end=num, withscores=True)
#     nnp_list = []
#     for e in nnp:
#         ts = str(e[1])
#         neg, neu, pos = e[0].decode('utf-8').split(' ')
#         nnp_list.append((ts, neg, neu, pos))
#     return nnp_list
#
# nnp_list = get_nnp(5)
# data = ""
# for nnp in nnp_list:
#     data += "[\"" + nnp[0] + "\"" + "," + nnp[1] + "," + nnp[2] + "," + nnp[3] + "]," + "\n"
#     print(data)

def get_wc(num):
    wc = red.zrevrange(name=redis_wc, start=0, end=num, withscores=True)
    wc_list = []
    for e in wc:
        word = e[0].decode('utf-8')
        count = str(e[1])
        wc_list.append((word, count))
    return wc_list

# wc_list = get_wc(20)
# # data = ""
# # i = 0
# # for wc in wc_list:
# #     i += 1
# #     data += "{\"x\":" + "\"" + wc[0] + "\"," + "\"value\":" + wc[1] + ", category: " + "\"Color" + str(i%4+1) + "\"},\n"
# #     print(data)

def assemble_wc():
    top_html = """
        <!doctype html>
        <html lang="en">
         <head>
          <meta charset="UTF-8">
          <meta content="IE=edge" http-equiv="X-UA-Compatible">
          <meta content="width=device-width, initial-scale=1" name="viewport">
          <title>JavaScript Tag Cloud Chart</title>
          <link href="https://playground.anychart.com/Nndi51Dr/iframe" rel="canonical">
          <meta content="Tag Cloud,Weighted List Chart,Word Cloud,Tooltip" name="keywords">
          <meta content="AnyChart - JavaScript Charts designed to be embedded and integrated" name="description">
          <!--[if lt IE 9]>
        <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
        <![endif]-->
          <style>html, body, #container {
            width: 700px;
            height: 500px;
            margin: 0;
            padding: 0;
        }</style>
         </head>
         <body>
          <div id="container"></div>
          <script src="js/anychart-base.min.js"></script>
          <script src="js/anychart-tag-cloud.min.js"></script>
          <script type="text/javascript">anychart.onDocumentReady(function () {

          var data = [
    """
    wc_list = get_wc(20)
    data = ""
    i = 0
    for wc in wc_list:
        i += 1
        data += "{\"x\":" + "\"" + wc[0] + "\"," + "\"value\":" + wc[1] + ", category: " + "\"Color" + str(
            int(i / 4) + 1) + "\"},\n"
    data = data[:-2]

    bottom_html = """];
        // create a tag cloud chart
        var chart = anychart.tagCloud(data);

        // set the chart title
        chart.title('Word Cloud: 20 Most Frequently Mentioned Words')
        // set array of angles, by which words will be placed
        chart.angles([0, -45, 90])
        // enable color range
        chart.colorRange(true);
        // set color range length
        chart.colorRange().length('80%');

        // format tooltips
        var formatter = "{%value}{scale:(1)(1000)(1000)(1000)|()( thousand)( million)( billion)}";
        var tooltip = chart.tooltip();
        tooltip.format(formatter);

        // display chart
        chart.container("container");
        chart.draw();
        });</script>
        </body>
        </html>
    """
    return top_html + data + bottom_html

print(assemble_wc())