# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from flask import *
import warnings
warnings.filterwarnings("ignore")
import psycopg2
import psycopg2.extras
from config import *
import time

app = Flask(__name__)
app.config.from_object(__name__)


# 链接数据库
def connectdb():
    db = psycopg2.connect(host = HOST, user = USER, password = PASSWORD, database = DATABASE)
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return (db,cursor)

# 关闭数据库
def closedb(db,cursor):
    db.close()
    cursor.close()

# 首页
@app.route('/')
def index():
    return render_template('index.html')
# 统计列表
@app.route('/list')
def list():
    (db,cursor) = connectdb()
    cursor.execute("select username, sum(start_num) AS sum_start, sum(mana_time) AS sum_mana, sum(beyond_time) AS sum_beyond, grade, assistant from public.doct_effe group by username, grade,assistant;")
    posts = cursor.fetchall()
    closedb(db,cursor)
    return render_template('list.html', posts = posts)

# 提交成功
@app.route('/submit')
def submit():
    return render_template('submit.html')

# 处理提交
@app.route('/handle', methods = ['POST'])
def handle():
    data = request.form.to_dict()
    (db,cursor) = connectdb()
    cursor.execute('''insert into doct_effe(username, start_num, mana_time, beyond_time, grade, assistant) values(%s, %s, %s, %s, %s, %s);''', [data['username'], data['start_num'], data['mana_time'],data['beyond_time'],data['grade'],data['assistant']])
    db.commit()
    closedb(db,cursor)
    return redirect(url_for('submit'))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
