from flask import Flask, render_template, request

from hidden import hidden

app = Flask(__name__)
app.register_blueprint(hidden, url_prefix='/m4st3rfully_h1dd3n')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/blogpost')
def blogpost():
    post_id = request.args.get('id')

    if 'flag' in post_id or '.py' in post_id or 'source.zip' in post_id:
        return render_template("nope.html"), 403

    ## Hacky passwd since heroku does not like overwriting root files..
    if '../../' in post_id and '/etc/passwd' in post_id:
        with app.open_resource("fake_passwd.txt") as f:
            blogpost_text = f.read().decode()

        return render_template("blogpost.html", blogpost_id=post_id, blogpost_text=blogpost_text)
    ## End Hacky passwd

    try:
        with app.open_resource(f"blogposts/{post_id}") as f:
            blogpost_text = f.read().decode()

        return render_template("blogpost.html", blogpost_id=post_id, blogpost_text=blogpost_text)
    except FileNotFoundError:
        return render_template("blogpost_404.html"), 404
