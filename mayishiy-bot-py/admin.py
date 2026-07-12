import json
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session

import config
import db as dbmod

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return wrapper


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form.get("username") == config.ADMIN_USER and request.form.get("password") == config.ADMIN_PASS:
            session["is_admin"] = True
            return redirect(url_for("admin.products_list"))
        error = "Login yoki parol noto'g'ri"
    return render_template("admin/login.html", error=error)


@admin_bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/")
@login_required
def products_list():
    rows = dbmod.query(
        """SELECT p.*, b.name AS brand_name, c.name AS category_name
           FROM products p
           JOIN brands b ON p.brand_id = b.id
           JOIN categories c ON b.category_id = c.id
           ORDER BY p.created_at DESC"""
    )
    return render_template("admin/products.html", products=rows)


# ---------- Kategoriyalar ----------

@admin_bp.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    if request.method == "POST":
        dbmod.execute(
            "INSERT INTO categories (name, sort_order) VALUES (?, ?)",
            (request.form["name"], request.form.get("sort_order") or 0),
        )
        return redirect(url_for("admin.categories"))
    rows = dbmod.query("SELECT * FROM categories ORDER BY sort_order, name")
    return render_template("admin/categories.html", categories=rows)


@admin_bp.route("/categories/<int:cat_id>/delete", methods=["POST"])
@login_required
def delete_category(cat_id):
    dbmod.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
    return redirect(url_for("admin.categories"))


# ---------- Brendlar ----------

@admin_bp.route("/brands", methods=["GET", "POST"])
@login_required
def brands():
    if request.method == "POST":
        dbmod.execute(
            "INSERT INTO brands (name, category_id) VALUES (?, ?)",
            (request.form["name"], request.form["category_id"]),
        )
        return redirect(url_for("admin.brands"))
    rows = dbmod.query(
        """SELECT b.*, c.name AS category_name FROM brands b
           JOIN categories c ON b.category_id = c.id ORDER BY c.name, b.name"""
    )
    categories = dbmod.query("SELECT * FROM categories ORDER BY sort_order, name")
    return render_template("admin/brands.html", brands=rows, categories=categories)


@admin_bp.route("/brands/<int:brand_id>/delete", methods=["POST"])
@login_required
def delete_brand(brand_id):
    dbmod.execute("DELETE FROM brands WHERE id = ?", (brand_id,))
    return redirect(url_for("admin.brands"))


# ---------- Mahsulotlar ----------

def parse_specs_text(specs_text):
    specs = {}
    for line in (specs_text or "").splitlines():
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            if key:
                specs[key] = value.strip()
    return specs


@admin_bp.route("/products/new", methods=["GET", "POST"])
@login_required
def new_product():
    brands = dbmod.query(
        """SELECT b.*, c.name AS category_name FROM brands b
           JOIN categories c ON b.category_id = c.id ORDER BY c.name, b.name"""
    )
    if request.method == "POST":
        specs = parse_specs_text(request.form.get("specs_text"))
        dbmod.execute(
            """INSERT INTO products (brand_id, model, price, description, specs, image_url, in_stock, is_promo)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                request.form["brand_id"],
                request.form["model"],
                request.form.get("price") or None,
                request.form.get("description", ""),
                json.dumps(specs, ensure_ascii=False),
                request.form.get("image_url") or None,
                1 if request.form.get("in_stock") else 0,
                1 if request.form.get("is_promo") else 0,
            ),
        )
        return redirect(url_for("admin.products_list"))
    return render_template("admin/product_form.html", brands=brands, product=None)


@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    brands = dbmod.query(
        """SELECT b.*, c.name AS category_name FROM brands b
           JOIN categories c ON b.category_id = c.id ORDER BY c.name, b.name"""
    )
    if request.method == "POST":
        specs = parse_specs_text(request.form.get("specs_text"))
        dbmod.execute(
            """UPDATE products SET brand_id=?, model=?, price=?, description=?,
               specs=?, image_url=?, in_stock=?, is_promo=? WHERE id=?""",
            (
                request.form["brand_id"],
                request.form["model"],
                request.form.get("price") or None,
                request.form.get("description", ""),
                json.dumps(specs, ensure_ascii=False),
                request.form.get("image_url") or None,
                1 if request.form.get("in_stock") else 0,
                1 if request.form.get("is_promo") else 0,
                product_id,
            ),
        )
        return redirect(url_for("admin.products_list"))

    rows = dbmod.query("SELECT * FROM products WHERE id = ?", (product_id,))
    if not rows:
        return redirect(url_for("admin.products_list"))
    product = dict(rows[0])
    product["specs"] = dbmod.parse_specs(product["specs"])
    return render_template("admin/product_form.html", brands=brands, product=product)


@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@login_required
def delete_product(product_id):
    dbmod.execute("DELETE FROM products WHERE id = ?", (product_id,))
    return redirect(url_for("admin.products_list"))
