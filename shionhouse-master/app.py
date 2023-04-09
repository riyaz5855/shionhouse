from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, LoginManager, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
# from flask_migrate import Migrate

# flask app and configs
app = Flask(__name__, template_folder='.', static_folder='assets')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'FsdkgnCJHKJbJgbvHGcHGChRtNbIh'
db = SQLAlchemy(app)
# migrate = Migrate(app, db)


# define the user_msg model
class UserMsg(db.Model):
    __tablename__ = "user_msg"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    message = db.Column(db.String(600), nullable=False)


# define the user data model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_no = db.Column(db.String(15), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
# define the newsletter model


@app.route('/phone')
def add_contact_no():
    if 'contact_no' not in User.__table__.columns:
        # Add phone_number column
        db.session.execute(
            'ALTER TABLE user ADD COLUMN contact_no VARCHAR(10)')
        db.session.commit()

        # Set phone_number to 11111 for all existing records
        users = User.query.all()
        for user in users:
            user.contact_no = '11111'
        db.session.commit()
        return "krgjelrkg"
    else:
        return "else"


class Newsletter(db.Model):
    __tablename__ = "newsletter"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)


# define the form data model
class Color(db.Model):
    __tablename__ = "color"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(7), nullable=False)

# define the size data model


class Size(db.Model):
    __tablename__ = "size"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# define the category data model


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# define the smry data model


class Smry(db.Model):
    __tablename__ = "smry"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    data = db.Column(db.String(2000), nullable=False)


# define the form data model
class Product(db.Model):
    __tablename__ = "roduct"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    sizes_prices = db.Column(db.String(200), nullable=False)
    colors = db.Column(db.String(1500), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    imageAdd = db.Column(db.String(600), nullable=False)


# # create the database
with app.app_context():
    db.create_all()

# admin panel
admin = Admin(app, name='Admin Panel', template_mode='bootstrap4')
admin.add_view(ModelView(UserMsg, db.session))
admin.add_view(ModelView(Newsletter, db.session))
admin.add_view(ModelView(Color, db.session))
admin.add_view(ModelView(Size, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Smry, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(User, db.session))


# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and current_user.is_admin:  # Check if user is already authenticated
        return redirect(url_for('sadmin'))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        try:
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    login_user(user)
                    print('login success')
                    return redirect(url_for('sadmin'))
        except ValueError as e:
            flash(str(e))
            return render_template('login.html')
            print('wrong pwd')
    return render_template('login.html')


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    print(request)
    if request.method == 'POST':
        print("reg")
        user_name = request.form['email']
        user_first_name = request.form['full_name']
        user_pwd1 = request.form['pwd1']
        user_pwd2 = request.form['pwd2']
        mob_no = request.form['mob_no']

        if user_pwd1 == user_pwd2:
            if User.query.filter_by(email=user_name).first():
                # messages.info(request, 'Email Taken')
                flash('Email Taken', 'info')
                print('Email Taken')
                return redirect('/home')
            else:
                user = User(
                    username=user_name, email=user_name, password=user_pwd1, contact_no=mob_no,)

                # profile = Profile.objects.create(
                #     user=user, refer_code=get_string(), contact_no=mob_no, )
                # Add the user to the database session
                db.session.add(user)

                # Commit the session to persist the changes to the database
                db.session.commit()

                print('user created')
                # profile.save()
                return redirect('/home')
        else:
            messages.info(request, 'Password not matching')
            print('Password not matching')
            return redirect('/login')
        return redirect('/')

    else:
        return redirect('/home')
# Set up the user loader function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/blog_details")
def blog_details():
    return render_template("blog_details.html")


@app.route("/elements")
def elements():
    return render_template("elements.html")


@app.route("/product_details")
def product_details():
    return render_template("product_details.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# users message
@app.route('/message', methods=['POST'])
def message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']

        msg = UserMsg(name=name, email=email, phone=phone,
                      subject=subject, message=message)
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('index'))


# newsletter
@app.route('/newsletter', methods=['POST'])
def newsletter():
    if request.method == 'POST':
        email = request.form['email']
        mail = Newsletter(email=email)
        db.session.add(mail)
        db.session.commit()
        return redirect(url_for('index'))
    return redirect(url_for('index'))


# admin login
@app.route('/sadmin')
@login_required
def sadmin():
    # if not current_user.is_admin:
    #     return redirect(url_for('login'))
    return render_template('sadmin.html')

# add product form


@app.route('/form', methods=['POST', 'GET'])
@login_required
def form():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        sizes = request.form.getlist('size')
        prices = [i for i in request.form.getlist('price') if i != '']
        sizes_prices = str(list(zip(sizes, prices)))

        colors = request.form.getlist('color')
        colors_list = []
        for color in colors:
            color_parts = color.split('-')
            colors_list.append(color_parts)
        colors_list = str(colors_list)

        description = str(request.form['description'])

        files = request.files.getlist('photo')
        # create a directory to store the files if it doesn't exist
        UPLOADS_FOLDER = os.path.join(app.static_folder, 'uploads')
        if not os.path.exists(UPLOADS_FOLDER):
            os.makedirs(UPLOADS_FOLDER)

        # loop through the files and save them to the server
        imageAdds = []
        for file in files:
            # generate a unique filename using timestamp and random string
            unique_filename = str(datetime.utcnow().timestamp()) + \
                '_' + str(random.randint(1, 10000))
            file_path = os.path.join('static/uploads', unique_filename)
            file.save(file_path)
            imageAdds.append(unique_filename)

        imageAddss = str(imageAdds)
        product = Product(name=name, category=category, sizes_prices=sizes_prices,
                          colors=colors_list, description=description, imageAdd=imageAddss)
        db.session.add(product)
        db.session.commit()

    color_data = Color.query.all()
    size_data = Size.query.all()
    category_data = Category.query.all()
    return render_template('form.html', color_data=color_data, size_data=size_data, category_data=category_data)


# color size form
@app.route('/colorsizeform', methods=['POST', 'GET'])
@login_required
def colorsizeform():
    if request.method == 'POST':
        if "color" in request.form.keys():
            # get the form values
            name = request.form['name']
            number = int(request.form['number'])
            color = request.form['color']

            # create a new form data object
            color_data = Color(name=name, number=number, color=color)

            # add the form data to the database
            db.session.add(color_data)
            db.session.commit()

        elif "size" in request.form.keys():
            name = request.form['size']
            size = Size(name=name)
            db.session.add(size)
            db.session.commit()

        elif "category" in request.form.keys():
            name = request.form['category']
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()

    # render a thank you message
    return render_template('colorsizeform.html')

# Define a Flask view for the '/admin' endpoint


@app.route('/admin')
@login_required
def admin():
    if current_user.is_authenticated and current_user.is_admin:
        # Render the default Flask-Admin index template
        return redirect('/admin/')
    else:
        # Redirect non-admin users to the login page
        return redirect(url_for('login'))

# dsb page


@app.route('/dsb')
@login_required
def dsb():
    products = Product.query.all()
    products_stl = []
    for product in products:
        l = stl(product)
        products_stl.append(l)
    return render_template('dsb.html', products=products_stl)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
