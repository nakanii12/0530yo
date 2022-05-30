import json
import requests
def get_data(videoid):
    t = json.loads(requests.get(r"https://vid.puffyan.us/api/v1/videos/"+ videoid).text)
    return [{"id":i["videoId"],"title":i["title"]} for i in t["recommendedVideos"]],t["formatStreams"][-1]["url"],t["descriptionHtml"].replace("\n","<br>"),t["title"]

def get_search(q):
    t = json.loads(requests.get(r"https://vid.puffyan.us/api/v1/search?q="+ q).text)
    return [{"title":i["title"],"id":i["videoId"]} for i in t]

from flask import Flask,render_template,request,abort,make_response

def check_cokie():
    if request.cookies.get('yuki', None) == "True":
        return True
    return False
    
app = Flask(__name__, static_folder='./static', static_url_path='')
@app.route("/")
def home():
    if check_cokie():
        return render_template("home.html")
    return """<head><title>計算機</title>
    <meta charset="utf-8">
</head>
<body>
<form action="/answer" method="get">
    <input type="text" name="q" required>
    <input type="submit" value="生成！！">
  <form name="dentaku">
    <table>
      <!-- 液晶画面部分 -->
      <tr>
        <td colspan="4">
          <input type="text" class="display" name="display" value="" disabled>
        </td>
      </tr>
 
      <!-- 上から1段目（7~9＋÷） -->
      <tr>
        <td><input type="button" value="7" onclick="get_calc(this)"></td>
        <td><input type="button" value="8" onclick="get_calc(this)"></td>
        <td><input type="button" value="9" onclick="get_calc(this)"></td>
        <td><input type="button" value="÷" class="operator" name="div_btn" onclick="get_calc(this)"></td>
      </tr>
        
      <!-- 上から2段目（4~6＋×） -->
      <tr>
        <td><input type="button" value="4" onclick="get_calc(this)"></td>
        <td><input type="button" value="5" onclick="get_calc(this)"></td>
        <td><input type="button" value="6" onclick="get_calc(this)"></td>
        <td><input type="button" value="×" class="operator" name="multi_btn" onclick="get_calc(this)"></td>
      </tr>
 
      <!-- 上から3段目（1~3＋-） -->
      <tr>
        <td><input type="button" value="1" onclick="get_calc(this)"></td>
        <td><input type="button" value="2" onclick="get_calc(this)"></td>
        <td><input type="button" value="3" onclick="get_calc(this)"></td>
        <td><input type="button" value="-" class="operator" onclick="get_calc(this)"></td>
      </tr>
 
      <!-- 上から4段目（0/C/=/+) -->
      <tr>
        <td><input type="button" value="0" onclick="get_calc(this)"></td>
        <td><input type="button" value="C" onclick="get_calc(this)"></td>
        <td><input type="button" value="=" class="equal" onclick="get_calc(this)"></td>
        <td><input type="button" value="+" class="operator" onclick="get_calc(this)"></td>
      </tr>
 
    </table>
  </form>
</body>
<script>
    function get_calc(btn) {
      if(btn.value == "=") {
        document.dentaku.display.value = eval(document.dentaku.display.value);
      } else if (btn.value == "C") {
        document.dentaku.display.value = "";
      } else {
        if (btn.value == "×") {
          btn.value = "*";
        } else if (btn.value == "÷") {
          btn.value = "/";
        } 
        document.dentaku.display.value += btn.value;
        document.dentaku.multi_btn.value = "×";
        document.dentaku.div_btn.value = "÷";
      }
    }
  </script>"""

@app.route('/watch')
def video():
    if not(check_cokie()):
        return <p>Cookieを許可してね</p>
    videoid = request.args.get("v")
    t = get_data(videoid)
    return render_template('video.html',videoid=videoid,videourl=t[1],res=t[0],description=t[2],videotitle=t[3])

@app.route("/search")
def search():
    if not(check_cokie()):
        return <p>Cookieを許可してね</p>
    q = request.args.get("q")
    return render_template("search.html",results=get_search(q))

@app.route("/answer")
def set_cokie():
    q = request.args.get("q")
    response = make_response("<head><title>電卓</title></head><body>"+" ".join([str(i) for i in range(int(q))])+"</body>")
    if q == "090328":
        response.set_cookie("yuki",value="True")
    return response

@app.errorhandler(404)
def page_not_found(error):
    return """<head><title>計算機</title>
    <meta charset="utf-8">
</head>
<body>
<form action="/answer" method="get">
    <input type="text" name="q" required>
    <input type="submit" value="生成！！">
  <form name="dentaku">
    <table>
      <!-- 液晶画面部分 -->
      <tr>
        <td colspan="4">
          <input type="text" class="display" name="display" value="" disabled>
        </td>
      </tr>
 
      <!-- 上から1段目（7~9＋÷） -->
      <tr>
        <td><input type="button" value="7" onclick="get_calc(this)"></td>
        <td><input type="button" value="8" onclick="get_calc(this)"></td>
        <td><input type="button" value="9" onclick="get_calc(this)"></td>
        <td><input type="button" value="÷" class="operator" name="div_btn" onclick="get_calc(this)"></td>
      </tr>
        
      <!-- 上から2段目（4~6＋×） -->
      <tr>
        <td><input type="button" value="4" onclick="get_calc(this)"></td>
        <td><input type="button" value="5" onclick="get_calc(this)"></td>
        <td><input type="button" value="6" onclick="get_calc(this)"></td>
        <td><input type="button" value="×" class="operator" name="multi_btn" onclick="get_calc(this)"></td>
      </tr>
 
      <!-- 上から3段目（1~3＋-） -->
      <tr>
        <td><input type="button" value="1" onclick="get_calc(this)"></td>
        <td><input type="button" value="2" onclick="get_calc(this)"></td>
        <td><input type="button" value="3" onclick="get_calc(this)"></td>
        <td><input type="button" value="-" class="operator" onclick="get_calc(this)"></td>
      </tr>
 
      <!-- 上から4段目（0/C/=/+) -->
      <tr>
        <td><input type="button" value="0" onclick="get_calc(this)"></td>
        <td><input type="button" value="C" onclick="get_calc(this)"></td>
        <td><input type="button" value="=" class="equal" onclick="get_calc(this)"></td>
        <td><input type="button" value="+" class="operator" onclick="get_calc(this)"></td>
      </tr>
 
    </table>
  </form>
</body>
<script>
    function get_calc(btn) {
      if(btn.value == "=") {
        document.dentaku.display.value = eval(document.dentaku.display.value);
      } else if (btn.value == "C") {
        document.dentaku.display.value = "";
      } else {
        if (btn.value == "×") {
          btn.value = "*";
        } else if (btn.value == "÷") {
          btn.value = "/";
        } 
        document.dentaku.display.value += btn.value;
        document.dentaku.multi_btn.value = "×";
        document.dentaku.div_btn.value = "÷";
      }
    }
  </script>"""
