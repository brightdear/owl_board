import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy # DB 도구 추가
from datetime import datetime
import pytz

app = Flask(__name__)

# 데이터베이스 파일 위치 설정 (프로젝트 폴더 안에 owl.db라는 파일이 생깁니다)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'owl.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 게시글 테이블 구조 정의
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.String(10), nullable=False)

# 앱 실행 시 DB 파일이 없으면 자동으로 만들어줍니다
with app.app_context():
    db.create_all()

def is_owl_time():
    tz = pytz.timezone('Asia/Seoul')
    current_hour = datetime.now(tz).hour
    if current_hour >= 5 or current_hour < 4:
        return True
    return False

@app.route('/')
def home():
    if is_owl_time():
        all_posts = Post.query.order_by(Post.id.desc()).all()
        return render_template('index.html', posts=all_posts)
    else:
        # 기존의 "<h1>...</h1>" 대신 아래 코드로 교체!
        return render_template('daytime.html')

@app.route('/post', methods=['POST'])
def post():
    nickname = request.form.get('nickname')
    content = request.form.get('content')
    if nickname and content:
        # --- 여기를 수정합니다 ---
        tz = pytz.timezone('Asia/Seoul') # 한국 시간대 설정
        korea_time = datetime.now(tz).strftime('%H:%M') # 한국 시간으로 현재 시각 가져오기
        
        new_post = Post(
            nickname=nickname, 
            content=content, 
            time=korea_time # 수정된 시간을 저장
        )
        # -----------------------
        db.session.add(new_post)
        db.session.commit()
    return redirect('/')
    