"""
CyberBlog - demo blog with an embedded unsafe deserialization bug inside a cookie.

IMPORTANT:
- This contains an intentional vulnerability: the app will base64-decode and
  call pickle.loads() on the value of the 'userdata' cookie (if present).
- This is for LAB ONLY. Do not expose publicly.

I WILL NOT provide exploit payloads. Use this app in an isolated environment.
"""
from flask import Flask, render_template, request, redirect, url_for, make_response, g, abort
import base64
import pickle        # used intentionally in one code path (UNSAFE)
import os

from extensions import db
from models import Post

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyberblog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    db.init_app(app)

    # ------------------------------------------------------------------
    # Hidden vulnerability:
    # On each request, we look for a cookie named 'userdata'. If present, we
    # decode base64 and call pickle.loads() — this is intentionally unsafe and
    # represents a subtle developer mistake where a cookie is treated as trusted.
    # ------------------------------------------------------------------
    @app.before_request
    def load_userdata_cookie():
        g.userdata = None
        b64 = request.cookies.get('userdata')
        if not b64:
            return
        try:
            raw = base64.b64decode(b64)
        except Exception:
            # treat as absent if invalid base64
            return
        try:
            # ====== UNSAFE OPERATION (INTENTIONAL for lab) =======
            # WARNING: pickle.loads on untrusted input can lead to code execution.
            obj = pickle.loads(raw)
            # store only basic info for templates, avoid exposing internals
            g.userdata = {'type': type(obj).__name__, 'repr': repr(obj)[:200]}
        except Exception:
            # deserialization errors are ignored (so site behaves normally)
            g.userdata = None

    # ------------------------------------------------------------------
    # Public routes (blog)
    # ------------------------------------------------------------------
    @app.route("/")
    def index():
        posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
        return render_template("index.html", posts=posts)

    @app.route("/posts")
    def posts():
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template("posts.html", posts=posts)

    @app.route("/post/<slug>")
    def post_detail(slug):
        p = Post.query.filter_by(slug=slug).first_or_404()
        return render_template("post_detail.html", post=p)

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/topics")
    def topics():
        # simple topic listing
        topics = db.session.query(Post.topic).distinct().all()
        topics = [t[0] for t in topics]
        return render_template("topics.html", topics=topics)

    # ------------------------------------------------------------------
    # Login route — sets a normal-looking 'userdata' cookie.
    # This models a developer who serialized a small dict to the cookie.
    # In a real site you'd use signed JSON; this is intentionally "developer mistake".
    # ------------------------------------------------------------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form.get("username", "visitor")
            # benign object we store in cookie (this is how site normally sets cookie)
            obj = {"username": username, "role": "reader"}
            raw = pickle.dumps(obj)               # insecure pattern used by dev
            b64 = base64.b64encode(raw).decode()
            resp = make_response(redirect(url_for('index')))
            # set cookie with HttpOnly False here to simulate a normal oversight (lab)
            resp.set_cookie('userdata', b64, httponly=False, samesite='Lax')
            return resp
        return render_template("login.html")

    # ------------------------------------------------------------------
    # Admin-style endpoint to clear cookie (safe utility)
    # ------------------------------------------------------------------
    @app.route("/logout")
    def logout():
        resp = make_response(redirect(url_for('index')))
        resp.delete_cookie('userdata')
        return resp

    # 404 handler
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html"), 404

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        # populate sample posts if empty
        try:
            from sample_data import insert_sample_posts
            insert_sample_posts(db)
        except Exception:
            pass
    # bind to all interfaces so Docker host mapping works
    app.run(host="0.0.0.0", port=5000, debug=True)

