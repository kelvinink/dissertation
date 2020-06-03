# Providing load balance for sentiment analysis module
import sys
import redis
import requests
from flask import Flask, request, send_from_directory
from datetime import datetime

app = Flask(__name__, static_url_path='')

##################### Configuration #####################
red = redis.Redis(host='localhost', port=6379, db=0)
redis_wc = 'word_cloud'
redis_nnp = 'nnp'
redis_ps = 'ps'
##################### Configuration #####################

def get_ps():
    ps = red.get(redis_ps)
    count, duration = ps.decode('utf-8').split(' ')
    return int(count), float(duration)

def get_wc(num):
    wc = red.zrevrange(name=redis_wc, start=0, end=num, withscores=True)
    wc_list = []
    for e in wc:
        word = e[0].decode('utf-8')
        count = str(e[1])
        wc_list.append((word, count))
    return wc_list

def get_nnp(num):
    nnp = red.zrevrange(name=redis_nnp, start=0, end=num, withscores=True)
    nnp_list = []
    for e in nnp:
        ts = str(e[1])
        neg, neu, pos = e[0].decode('utf-8').split(' ')
        nnp_list.append((ts, neg, neu, pos))
    return nnp_list


def assemble_ps():
    count, duration = get_ps()
    return """
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load("current", {"packages":["table"]});
      google.charts.setOnLoadCallback(drawTable);
      function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn("number", "#Tweets");
        data.addColumn("number", "Duration");
        data.addColumn("number", "Process Speed (tweets/sec)");
        data.addRows([
          [""" + str(count) + "," + str(duration) + "," +  str(count/duration) +  """],
        ]);
        var table = new google.visualization.Table(document.getElementById("table_div"));
        table.draw(data, {showRowNumber: true, width: "700px", height: "80px"});
      }
    </script>
    """

def assemble_nnp():
    top_html = """
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load("current", {"packages":["corechart"]});
      google.charts.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
          ["Timestamp",  "Neu", "Neg", "Pos"],
    """

    nnp_list = get_nnp(20)
    data = ""
    for nnp in nnp_list:
        ts = str(datetime.utcfromtimestamp(int(float(nnp[0]))).strftime('%Y-%m-%d %H:%M:%S'))
        data += "[\"" + ts + "\"" + "," + nnp[2] + "," + nnp[1] + "," + nnp[3] + "]," + "\n"

    bottom_html = """]);
        var options = {
          title: "Cryptocurrency Sentiment Trend",
          vAxis: {title: "Percentage"},
          isStacked: true
        };
        var chart = new google.visualization.SteppedAreaChart(document.getElementById("chart_div"));
        chart.draw(data, options);
      }
    </script>
    """

    return top_html + data + bottom_html

def assemble_wc():
    top_html = """
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
    """
    return top_html + data + bottom_html

def assemble_dashboard():
    head_html = """
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
            width: 800px;
            height: 600px;
            margin: 0;
            padding: 0;}
            
            .center {
              display: block;
              margin-left: auto;
              margin-right: auto;
              width: 50%;
            }
          </style>
         </head>
         <body>
          <div id="table_div" class="center"></div>
          <div id="container" class="center"></div>
          <div id="chart_div" style="width: 1300px; height: 500px;" class="center"></div>
    """
    dashboard_ps = assemble_ps()
    dashboard_nnp = assemble_nnp()
    dashboard_wc = assemble_wc()

    foot_html = """
        </body>
        </html>
    """

    return head_html + dashboard_ps + dashboard_nnp + dashboard_wc + foot_html

@app.route('/api/rcas/dashboard', methods=['GET'])
def dashboard():
    return assemble_dashboard()


@app.route('/api/rcas/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=88)
