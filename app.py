import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "replace_me"

# ---- Config your gallery folder under /static ----
GALLERY_SUBDIR = "images/food"   # i.e., static/images/food/...
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".avif"}

def get_gallery_images():
    """
    Return list of static-relative paths like 'images/food/xyz.jpg',
    sorted newest first (fallback to name).
    """
    base = os.path.join(app.static_folder, GALLERY_SUBDIR)
    if not os.path.isdir(base):
        return []
    files = []
    for root, _, names in os.walk(base):
        for n in names:
            ext = os.path.splitext(n)[1].lower()
            if ext in ALLOWED_EXTS:
                abs_path = os.path.join(root, n)
                rel_from_static = os.path.relpath(abs_path, app.static_folder).replace("\\", "/")
                files.append(rel_from_static)
    files.sort(key=lambda p: (os.path.getmtime(os.path.join(app.static_folder, p)), p), reverse=True)
    return files

# ---- Routes ----
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/what-we-offer")
def what_we_offer():
    images = get_gallery_images()
    # Debug prints (optional)
    print("[what_we_offer] static folder:", app.static_folder)
    print("[what_we_offer] subdir:", GALLERY_SUBDIR)
    print("[what_we_offer] found images:", len(images))
    return render_template("what_we_offer.html", images=images)

@app.route("/gallery")
def gallery():
    images = get_gallery_images()
    # Decide where “Back” should go
    back_url = url_for('what_we_offer') if 'what_we_offer' in app.view_functions else url_for('home')
    return render_template("gallery.html", images=images, back_url=back_url)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        event_type = request.form.get("event_type")
        guests = request.form.get("guests")
        message = request.form.get("message")
        # TODO: email/store the submission
        flash("Thanks! We got your inquiry and will reply soon.")
        return redirect(url_for("contact"))
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)
