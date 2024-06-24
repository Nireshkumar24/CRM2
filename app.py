
from sqlite3 import IntegrityError
from flask import Flask, jsonify, render_template, request, redirect, send_from_directory, url_for,flash,session,send_file,abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import String, cast, create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from flask_migrate import Migrate
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime, date
# from twilio.rest import Client
# from flask_mail import Message,Mail
from werkzeug.utils import secure_filename
from uuid import uuid4
import zipfile
import io

UPLOAD_FOLDER = './upload_folder'


# Your Flask app and route definitions follow here
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'fd9bb9b8ee91aee5b1957e8ef313545aeff15aa3bada'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



db = SQLAlchemy(app)
migrate = Migrate(app, db)

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'nireshkumarniresh@gmail.com'
# app.config['MAIL_PASSWORD'] = 'rfnl gfmp espw oyyf'
# mail = Mail(app)

# twilio_account_sid = 'AC1de0cac0890355675dbbbc0cd9dd81f6'
# twilio_auth_token = 'a81dcac8e4e30b6572ce0a92c1d06084'
# twilio_client = Client(twilio_account_sid, twilio_auth_token)



class UserDetails(db.Model):
    __tablename__ = 'user_details'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    mobile_number = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(300), nullable=False)


class AddCategory(db.Model):
    __tablename__ = 'add_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(300), nullable=False)
   
class UserActivity(db.Model):
    __tablename__ = 'user_activity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    followup = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(300), nullable=True)
   
class Admin(db.Model):
    __tablename__='admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    contact = db.Column(db.String(100), nullable=False)  # Corrected datatype
    email = db.Column(db.String(100), nullable=False)  # Corrected datatype
    unique_link = db.Column(db.String(255), unique=True, nullable=True)  # Adding unique_link field


with app.app_context():
    db.create_all() 

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Placeholder validation logic
        if username == 'Niresh24' and password == 'password':
            session['username'] = username
            return redirect(url_for('addcategory'))
        else:
            msg = 'Invalid email or password. Please try again.'
            return render_template('login.html', msg=msg)
    return render_template('login.html')  


# @app.route('/adduser', methods=['GET', 'POST'])
# def adduser():
#     if request.method == 'POST':
#         try:
#             new_customer = UserDetails(
#                 customer_name=request.form['cname'],
#                 email=request.form['email'],
#                 mobile_number=request.form['mobileNumber'],
#                 location=request.form['location'],
#             )
#             db.session.add(new_customer)
#             db.session.commit()
#             return redirect(url_for('addcategory'))
#         except Exception as e:
#             db.session.rollback()
#             print("Failed to add customer:", e)
#             return render_template('adduser.html', error="An error occurred: " + str(e))

#     page = request.args.get('page', 1, type=int)
#     per_page = 10
#     pagination = UserDetails.query.paginate(page=page, per_page=per_page, error_out=False)
#     customers = pagination.items
#     return render_template('adduser.html', customers=customers, pagination=pagination)
@app.route('/adduser', methods=['GET', 'POST'])
def adduser():
    if request.method == 'POST':
        try:
            new_customer = UserDetails(
                customer_name=request.form['cname'],
                email=request.form['email'],
                mobile_number=request.form['mobileNumber'],
                location=request.form['location'],
            )
            db.session.add(new_customer)
            db.session.commit()
            return redirect(url_for('adduser'))
        except Exception as e:
            db.session.rollback()
            print("Failed to add customer:", e)
            page = request.args.get('page', 1, type=int)
            per_page = 10
            pagination = UserDetails.query.paginate(page=page, per_page=per_page, error_out=False)
            customers = pagination.items
            return render_template('adduser.html', customers=customers, pagination=pagination, error="An error occurred: " + str(e))

    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = UserDetails.query.paginate(page=page, per_page=per_page, error_out=False)
    customers = pagination.items
    return render_template('adduser.html', customers=customers, pagination=pagination)


# @app.route('/addcategory', methods=['GET', 'POST'])
# def addcategory():
#     if request.method == 'POST':
#         new_category = AddCategory(category=request.form['category'])
#         db.session.add(new_category)
#         db.session.commit()
#         return redirect(url_for('index'))
#     categories = AddCategory.query.all()
#     return render_template('addcategory.html', categories=categories)

@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if request.method == 'POST':
        new_category = AddCategory(category=request.form['category'])
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = AddCategory.query.paginate(page=page, per_page=per_page, error_out=False)
    categories = pagination.items
    return render_template('addcategory.html', categories=categories, pagination=pagination)

# @app.route('/index', methods=['GET','POST'])
# def index():
#     followup_count = get_followup_notification_count()
#     if request.method == 'POST':
#         try:
            
#             followup_datetime = datetime.strptime(request.form.get('followup'), '%Y-%m-%dT%H:%M') if request.form.get('followup') else None
        
#             new_activity = UserActivity(
#                 customer_name=request.form.get('customerName'),
#                 category=request.form.get('category'),
#                 followup=followup_datetime,
#                 status=request.form.get('status'),
#                 description = request.form.get('description'),
#             )
#             db.session.add(new_activity)
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#         return redirect(url_for('index'))
#     user_activities = UserActivity.query.all()
#     categories = AddCategory.query.all()
#     all_customers = UserDetails.query.all()
#     return render_template('index.html',categories=categories, customers=all_customers, user_activities= user_activities,followup_count=followup_count)

@app.route('/index', methods=['GET', 'POST'])
def index():
    followup_count = get_followup_notification_count()
    if request.method == 'POST':
        try:
            followup_datetime = datetime.strptime(request.form.get('followup'), '%Y-%m-%dT%H:%M') if request.form.get('followup') else None
            new_activity = UserActivity(
                customer_name=request.form.get('customerName'),
                category=request.form.get('category'),
                followup=followup_datetime,
                status=request.form.get('status'),
                description=request.form.get('description'),
            )
            db.session.add(new_activity)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print("Failed to add activity:", e)
            return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = UserActivity.query.paginate(page=page, per_page=per_page, error_out=False)
    user_activities = pagination.items
    categories = AddCategory.query.all()
    all_customers = UserDetails.query.all()

    return render_template('index.html', categories=categories, customers=all_customers,
                           user_activities=user_activities, followup_count=followup_count, pagination=pagination)



@app.route('/useractivity/<int:activity_id>')
def useractivity_detail(activity_id):
    activity = UserActivity.query.get(activity_id)
    if activity is None:
        abort(404)  # Not found
    return render_template('useractivity_details.html', activity=activity)

    #   delete and edit sections


@app.route('/edit_category/<int:id>', methods=['POST'])
def edit_category(id):
    category = AddCategory.query.get_or_404(id)
    category.category = request.form['category']
    db.session.commit()
    return redirect(url_for('addcategory'))

@app.route('/delete_category/<int:id>', methods=['POST'])
def delete_category(id):
    category = AddCategory.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('addcategory'))


@app.route('/edit_customer/<int:id>', methods=['POST'])
def edit_customer(id):
    customer = UserDetails.query.get_or_404(id)
    customer.customer_name = request.form['cname']
    customer.email = request.form['email']
    customer.mobile_number = request.form['mobileNumber']  # Corrected attribute name
    customer.location = request.form['location']
    db.session.commit()
    
    # Fetch the updated pagination data
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = UserDetails.query.paginate(page=page, per_page=per_page, error_out=False)
    customers = pagination.items
    
    # Pass the updated data to the template
    return render_template('adduser.html', customers=customers, pagination=pagination)

@app.route('/delete_customer/<int:id>', methods=['POST'])
def delete_customer(id):
    customer = UserDetails.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return render_template('adduser.html')



# Route for editing an activity
@app.route('/edit_activity/<int:id>', methods=['POST'])
def edit_activity(id):
    activity = UserActivity.query.get_or_404(id)
    activity.customer_name = request.form.get('customerName')
    activity.category = request.form.get('category')
    activity.followup = datetime.strptime(request.form.get('followup'), '%Y-%m-%dT%H:%M')
    activity.status = request.form.get('status')
    activity.description = request.form.get('description')
    db.session.commit()
    return redirect(url_for('index'))

# Route for deleting an activity
@app.route('/delete_activity/<int:id>', methods=['POST'])
def delete_activity(id):
    activity = UserActivity.query.get_or_404(id)
    db.session.delete(activity)
    db.session.commit()
    return redirect(url_for('index'))

   ## search 
   
# @app.route('/search', methods=['POST'])
# def search():
#     search_query = request.form.get('search', '')
#     categories = AddCategory.query.filter(AddCategory.category.like('%' + search_query + '%')).all()
#     return render_template('addcategory.html', categories=categories)

@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search', '')
    page = request.args.get('page', 1, type=int)  # Get the current page number
    per_page = 10  # Set the number of items per page

    categories = AddCategory.query.filter(
        AddCategory.category.like(f'%{search_query}%')
    ).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('addcategory.html', categories=categories.items, pagination=categories)

# @app.route('/search_user', methods=['POST'])
# def search_user():
#     search_query = request.form.get('search', '')

#     try:
#         search_query_int = int(search_query)
#         id_condition = UserDetails.id == search_query_int
#     except ValueError:
#         id_condition = False

#     filtered_customers = UserDetails.query.filter(
#         or_(
#             id_condition,
#             UserDetails.customer_name.like(f'%{search_query}%'),
#             UserDetails.email.like(f'%{search_query}%'),
#             UserDetails.mobile_number.like(f'%{search_query}%'),
#             UserDetails.location.like(f'%{search_query}%'),
#             cast(UserDetails.id, String).like(f'%{search_query}%')  
#         )
#     ).all()
   
#     return render_template('adduser.html', customers=filtered_customers)   

@app.route('/search_user', methods=['POST'])
def search_user():
    search_query = request.form.get('search', '')
    page = request.args.get('page', 1, type=int)  # Get the current page number
    per_page = 10  # Set the number of items per page

    try:
        search_query_int = int(search_query)
        id_condition = (UserDetails.id == search_query_int)
    except ValueError:
        id_condition = False  # No valid integer, no ID condition

    # Use SQLAlchemy `or_` to combine search conditions
    if id_condition:
        conditions = [id_condition]
    else:
        conditions = [
            UserDetails.customer_name.like(f'%{search_query}%'),
            UserDetails.email.like(f'%{search_query}%'),
            UserDetails.mobile_number.like(f'%{search_query}%'),
            UserDetails.location.like(f'%{search_query}%'),
            cast(UserDetails.id, String).like(f'%{search_query}%')
        ]

    if conditions:
        filtered_customers = UserDetails.query.filter(or_(*conditions)).paginate(page=page, per_page=per_page, error_out=False)
    else:
        filtered_customers = UserDetails.query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template('adduser.html', customers=filtered_customers.items, pagination=filtered_customers)



# @app.route('/search_index', methods=['POST'])
# def search_index():
#     action = request.form.get('action', '')
#     followup_count = get_followup_notification_count()
#     if action == 'clear':
#         user_activities = UserActivity.query.all()
#     else:
#         search_query = request.form.get('search', '')
#         selected_category = request.form.get('category', '')
#         selected_status = request.form.get('status', '')

#         query_conditions = []

#         if search_query:
#             try:
#                 search_query_int = int(search_query)
#                 query_conditions.append(UserActivity.id == search_query_int)
#             except ValueError:
#                 pass 
            
#             query_conditions.extend([
#                 UserActivity.customer_name.like(f'%{search_query}%'),
#                 UserActivity.description.like(f'%{search_query}%')
#             ])

#         if selected_category and selected_category != "":
#             query_conditions.append(UserActivity.category == selected_category)
        
#         if selected_status and selected_status != "":
#             query_conditions.append(UserActivity.status == selected_status)

#         user_activities = UserActivity.query.filter(or_(*query_conditions)).all() if query_conditions else UserActivity.query.all()
#     return render_template('index.html', user_activities=user_activities, followup_count=followup_count)


# def get_followup_notification_count():
#     today = datetime.now().date()
#     notification_end_date = today + timedelta(days=3)
#     count = UserActivity.query.filter(UserActivity.followup >= today, UserActivity.followup <= notification_end_date).count()
#     return count


@app.route('/search_index', methods=['POST'])
def search_index():
    action = request.form.get('action', '')
    page = request.args.get('page', 1, type=int)  # Get the current page number
    per_page = 10  # Set the number of items per page

    if action == 'clear':
        user_activities = UserActivity.query.paginate(page=page, per_page=per_page, error_out=False)
    else:
        search_query = request.form.get('search', '')
        selected_category = request.form.get('category', '')
        selected_status = request.form.get('status', '')
        query_conditions = []

        if search_query:
            try:
                search_query_int = int(search_query)
                query_conditions.append(UserActivity.id == search_query_int)
            except ValueError:
                query_conditions.extend([
                    UserActivity.customer_name.like(f'%{search_query}%'),
                    UserActivity.description.like(f'%{search_query}%')
                ])

        if selected_category:
            query_conditions.append(UserActivity.category == selected_category)

        if selected_status:
            query_conditions.append(UserActivity.status == selected_status)

        if query_conditions:
            user_activities = UserActivity.query.filter(or_(*query_conditions)).paginate(page=page, per_page=per_page, error_out=False)
        else:
            user_activities = UserActivity.query.paginate(page=page, per_page=per_page, error_out=False)

    followup_count = get_followup_notification_count()
    return render_template('index.html', user_activities=user_activities.items, pagination=user_activities, followup_count=followup_count)

def get_followup_notification_count():
    today = datetime.now().date()
    notification_end_date = today + timedelta(days=3)
    count = UserActivity.query.filter(UserActivity.followup >= today, UserActivity.followup <= notification_end_date).count()
    return count

@app.route('/notifications')
def notifications():
    today = datetime.today().date()
    today_activities = UserActivity.query.filter(
        db.func.date(UserActivity.followup) == today
    ).all()
    activities_data = [{
        'id': activity.id,
        'customer_name': activity.customer_name,
        'followup': activity.followup.strftime('%Y-%m-%d %H:%M')
    } for activity in today_activities]

    return jsonify(activities_data)


@app.route('/createuser',methods=['GET','POST'])
def createuser():
    if request.method == 'POST':
            admin=Admin(
               username=request.form['username'],
               password=request.form['password'],
               contact = request.form['contact'],
               email = request.form['email']   
           )
            db.session.add(admin)
            db.session.commit()
            return (url_for('createuser'))
    users=Admin.query.all()    
    return render_template('admincreate2.html',users=users)

@app.route('/edit_user/<int:id>', methods=['POST'])
def edit_user(id):
    user = Admin.query.get_or_404(id)
    user.username = request.form['username']
    user.password = request.form['password']
    user.contact = request.form['contact']
    user.email = request.form['email']

    db.session.commit()
    flash('User updated successfully.', 'success')
    return redirect(url_for('createuser'))  


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    user = Admin.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('createuser'))  # Redirecting to 'createuser' to see the changes

@app.route('/user_search', methods=['POST'])
def user_search():
    search_query = request.form.get('search', '')
    try:
        search_query_int = int(search_query)
        id_condition = Admin.id == search_query_int
    except ValueError:
        id_condition = False

    filtered_users = Admin.query.filter(
        or_(
            id_condition,
            Admin.username.like(f'%{search_query}%'),
            Admin.password.like(f'%{search_query}%'),  # Consider security implications
            Admin.contact.like(f'%{search_query}%'),
            Admin.email.like(f'%{search_query}%'), 
            cast(Admin.id, String).like(f'%{search_query}%')  
        )
    ).all()
    return render_template('admincreate2.html', users=filtered_users)



@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Admin.query.filter_by(username=username).first()
        if user is not None and user.password == password:
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template('userlogin.html')
    return render_template('userlogin.html')

### send messages

# @app.route('/send_message/<int:user_id>')
# def send_message(user_id):
#     user = Admin.query.get(user_id)
#     if user:
#         # Send WhatsApp Message
#         message = "Hello, this is a message from your application."
#         twilio_client.messages.create(
#             body=message,
#             from_='whatsapp:+14155238886',
#             to=f'whatsapp:{user.contact}'  # Ensure 'contact' contains a valid WhatsApp number format
#         ) 
#         # Send Email
#         msg = Message('Hello', sender='nireshkumarniresh@gmail.com', recipients=[user.email])
#         msg.body = "This is for me"
#         mail.send(msg)
#         return 'Message sent!'
#     else:
#         return 'User not found!', 404


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




#-------------------------------------------

@app.route('/upload_documents/<int:user_id>', methods=['GET', 'POST'])
def upload_documents(user_id):
    user = UserDetails.query.get_or_404(user_id)
    if request.method == 'POST':
        documents = {
            'aadhar': request.files.get('aadhar'),
            'pan': request.files.get('pan'),
            'bank_statement': request.files.get('bank_statement'),
            'passbook': request.files.get('passbook'),
            'certificate': request.files.get('certificate')
        }

        # Ensure the upload folder for the specific user exists
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Process each document
        for doc_name, file in documents.items():
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                doc_path = os.path.join(user_folder, doc_name)  # Specific folder for each document type
                if not os.path.exists(doc_path):
                    os.makedirs(doc_path)
                file.save(os.path.join(doc_path, filename))

        flash('Documents uploaded successfully.')
        return redirect(url_for('upload_documents', user_id=user_id))

    return render_template('Upload.html', user_id=user_id)



@app.route('/user_profile/<int:user_id>')
def user_profile(user_id):
    user = UserDetails.query.get_or_404(user_id)
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
    documents = {}

    if os.path.exists(user_folder):
        for doc_type in ['aadhar', 'pan', 'bank_statement', 'passbook', 'certificate']:
            doc_folder = os.path.join(user_folder, doc_type)
            if os.path.exists(doc_folder):
                documents[doc_type] = [f for f in os.listdir(doc_folder) if os.path.isfile(os.path.join(doc_folder, f))]

    return render_template('Userprofile_customer.html', user=user, documents=documents)


@app.route('/view_document/<int:user_id>/<doc_type>/<filename>')
def view_document(user_id, doc_type, filename):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), doc_type)
    return send_from_directory(directory, filename)


@app.route('/generate_link/<int:user_id>')
def generate_link(user_id):
    user = UserDetails.query.get(user_id)
    if user is None:
        print(f"No user found with ID: {user_id}")
        return jsonify({'error': 'User not found'}), 404
    link = url_for('upload_documents', user_id=user_id, _external=True)
    return jsonify({'link': link})



@app.route('/delete_document/<int:user_id>/<doc_type>/<filename>', methods=['POST'])
def delete_document(user_id, doc_type, filename):
    try:
        path = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), doc_type, filename)
        os.remove(path)  # Remove the file
        flash('Document deleted successfully.', 'success')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('user_profile', user_id=user_id))

@app.route('/edit_document/<int:user_id>/<doc_type>/<filename>', methods=['POST'])
def edit_document(user_id, doc_type, filename):
    user = UserDetails.query.get_or_404(user_id)
    if 'new_document' in request.files:
        file = request.files['new_document']
        if file and allowed_file(file.filename):
            try:
                # Secure the filename and prepare paths
                filename_secure = secure_filename(file.filename)
                user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), doc_type)
                file_path = os.path.join(user_folder, filename_secure)

                # Remove the old file if it exists
                old_file_path = os.path.join(user_folder, filename)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

                # Save the new file
                file.save(file_path)
                flash('Document replaced successfully.')
            except Exception as e:
                flash(f'An error occurred: {str(e)}')
        else:
            flash('Invalid file type.')
    else:
        flash('No file provided.')

    return redirect(url_for('user_profile', user_id=user_id))

@app.route('/download_document/<int:user_id>/<doc_type>/<filename>')
def download_document(user_id, doc_type, filename):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id), doc_type)
    return send_from_directory(directory, filename, as_attachment=True)





@app.route('/download_all_documents/<int:user_id>')
def download_all_documents(user_id):
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(user_id))
    data = io.BytesIO()
    
    with zipfile.ZipFile(data, mode='w') as z:
        for folder_name in ['aadhar', 'pan', 'bank_statement', 'passbook', 'certificate']:
            folder_path = os.path.join(user_folder, folder_name)
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    # Ensure the archive path does not contain the absolute path
                    archive_name = os.path.join(folder_name, filename)
                    z.write(file_path, arcname=archive_name)
    
    data.seek(0)
    
    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        download_name=f'{user_id}_documents.zip'
    )

if __name__ == '__main__':
    app.run(port=5000, debug=True)