from flask import Flask, render_template, send_from_directory, abort, Response
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# Project root directory
ROOT = os.path.abspath(os.path.dirname(__file__))

# ---------- Routes ----------

@app.route("/")
def index():
    # Renders templates/index.html which shows the robot image
    return render_template("index.html")

@app.route("/robots.txt")
def robots():
    """
    Serve the robots.txt file from project root.
    This returns plain text.
    """
    robots_path = os.path.join(ROOT, "robots.txt")
    if not os.path.isfile(robots_path):
        # If missing, return a sensible default
        default = "User-agent: *\nDisallow: /s3cr3t_fl4g.txt\n"
        return Response(default, mimetype="text/plain")
    return send_from_directory(ROOT, "robots.txt", mimetype="text/plain")

@app.route("/s3cr3t_fl4g.txt")
def flag():
    """
    Serve the flag file (CTF intended). We explicitly send only the
    known filename from the project root to avoid path traversal risks.
    """
    flag_path = os.path.join(ROOT, "s3cr3t_fl4g.txt")
    if not os.path.isfile(flag_path):
        # Hide internals if flag missing
        abort(404)
    return send_from_directory(ROOT, "s3cr3t_fl4g.txt", mimetype="text/plain")

# Optional: safe catch-all for other files if you want to add more hints
# @app.route("/<path:subpath>")
# def show_subpath(subpath):
#     return abort(404)

# ---------- App runner ----------
if __name__ == "__main__":
    # Development server (use gunicorn for production)
    app.run(host="0.0.0.0", port=5000, debug=False)
