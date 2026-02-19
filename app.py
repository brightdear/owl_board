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
    # 테스트를 위해 현재 시간(오후 1시 이후)에도 열리도록 설정됨
    if current_hour >= 13 or current_hour < 4:
        return True
    return False

@app.route('/')
def home():
    if is_owl_time():
        # DB에서 최신순으로 글을 가져옵니다
        all_posts = Post.query.order_by(Post.id.desc()).all()
        return render_template('index.html', posts=all_posts)
    else:
        return "<h1>☀️ 해가 떠 있습니다!</h1><p>22:00에 다시 만나요.</p>"

@app.route('/post', methods=['POST'])
def post():
    nickname = request.form.get('nickname')
    content = request.form.get('content')
    if nickname and content:
        # DB에 새로운 글 저장
        new_post = Post(
            nickname=nickname, 
            content=content, 
            time=datetime.now().strftime('%H:%M')
        )
        db.session.add(new_post)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
    