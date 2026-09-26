
from flask import Flask,render_template,request,redirect,url_for,flash
from flask_login import LoginManager,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from config import Config
from models import db,User,Team,Member
app=Flask(__name__); app.config.from_object(Config); db.init_app(app)
lm=LoginManager(app); lm.login_view="login"
@lm.user_loader
def load(uid): return db.session.get(User,int(uid))
@app.route("/",methods=["GET","POST"])
def login():
    if request.method=="POST":
        u=User.query.filter_by(username=request.form["username"]).first()
        if u and u.active and check_password_hash(u.password,request.form["password"]):
            login_user(u); return redirect(url_for("dashboard"))
        flash("Invalid login")
    return render_template("login.html")
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html",teams=Team.query.all(),users=User.query.all())
@app.route("/logout")
def logout(): logout_user(); return redirect("/")
@app.route("/user",methods=["POST"])
@login_required
def user():
    if not current_user.is_admin: return ("Forbidden",403)
    db.session.add(User(username=request.form["u"],password=generate_password_hash(request.form["p"])))
    db.session.commit(); return redirect("/dashboard")
@app.route("/toggle/<int:uid>")
@login_required
def toggle(uid):
    if not current_user.is_admin: return ("Forbidden",403)
    u=db.session.get(User,uid); u.active=not u.active; db.session.commit(); return redirect("/dashboard")
@app.route("/scan/<code>",methods=["GET","POST"])
@login_required
def scan(code):
    t=Team.query.filter_by(qr_code=code).first()
    if not t:
        t=Team(qr_code=code,count=1); db.session.add(t); db.session.commit()
    if request.method=="POST":
        t.track=request.form["track"]; t.team_name=request.form["team"]; t.leader_name=request.form["leader"]
        t.roll=request.form["roll"]; t.institute=request.form["inst"]; t.location=request.form["loc"]
        t.phone=request.form["phone"]; t.count=int(request.form["count"])
        Member.query.filter_by(team_id=t.id).delete()
        for i in range(t.count):
            db.session.add(Member(team_id=t.id,name=request.form.get(f"m{i}"),roll=request.form.get(f"r{i}"),phone=request.form.get(f"p{i}")))
        db.session.commit(); flash("Saved"); return redirect(url_for("scan",code=code))
    return render_template("scan.html",t=t,code=code,m=t.members)
if __name__=="__main__": app.run(host="0.0.0.0",port=5000,debug=True)
