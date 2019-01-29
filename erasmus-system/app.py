from flask import Flask
from flask import request
from flask import render_template
from flask import g
from flask import url_for
from flask import redirect
from werkzeug.contrib.cache import SimpleCache
import sqlite3



"""
TO DO
i) find a way to differentiate menus for both students and admins
ii)

"""

"""
Helper

all_courses := all_courses - courses_not_learned

criteria_for_admittance = (courses >= all_courses - 5) &&
                          (year > 3) &&
                          (language not none)
"""

# Constant

admins = ['vasilis', 'petros']
all_courses_3rd_year = 32
all_coures_4th_year = 42

"""

Description of the webpage:

    Το πανεπιστήμιο διαθέτει ένα σύστημα ώστε να διαχειρίζεται τις ανταλλαγές φοιτητών μέσω του προγράμματος ανταλλαγής φοιτητών erasmus.

Kάθε συνεργαζόμενο πανεπιστήμιο έχει συγκεκριμένο αριθμό φοιτητών που μπορεί να δεχτεί  με μέγιστη διάρκεια ενός εξαμήνου. Ο προϊστάμενος της γραμματείας ενημερώνει το σύστημα για τα διαθέσιμα συνεργαζόμενα πανεπιστήμια καθώς και για διαθέσιμες θέσεις σε καθένα από αυτά στην αρχή κάθε εξαμήνου.

Τα κριτήρια για την επιλογή φοιτητή στο πλαίσιο ανταλλαγης erasmus  είναι τα εξής:

- να μη χρωστάει πάνω από 5 συνολικά μαθήματα
- να είναι στο 3ο ή 4ο έτος
- να γνωρίζει την ξένη γλώσσα η οποία διδάσκεται στο εκάστοτε πανεπιστήμιο της επιλογής του.

"""

# Initialize the app

app = Flask(__name__)
cache = SimpleCache()

# Initialize the db connection

conn = sqlite3.connect('users.db', check_same_thread=False, isolation_level=None)
c = conn.cursor()

with app.test_request_context('/login/', method='POST'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/login/'
    assert request.method == 'POST'

"""
--- User ----
username:0
password:1
courses:2
year:3
language:4
uni1:5
uni2:6
uni3:7
-----------

--- Uni ---
name:0
acceptances:1
language:2
------------
"""

# Pushes user to submissions db

"""
ISSUES:

i)VALUES DONT GET PUSHED TO DB

"""

def push_to_db(university):
    print(university)
    query = c.execute("update submissions set total_submits = total_submits + 1, accepted = accepted + 1, remaining = remaining - 1 where uni='%s'" % university)

    conn.commit()
    try:
        print('got in')
        
        return query
    except:
        return "failed"


# Returns a positive number for the remaining seats

def remaining_seats(university_name):
    query = c.execute("select remaining, uni from submissions where uni='%s'" % university_name)
    try:
        remaining = c.fetchone()
        print(remaining[0])
        if (remaining[0]):
            push_to_db(remaining[1])
        else:
            print(remaining[1] + " Doesn't have seats left")
            return 0
        return 

    except:

        return -1

# Checks if the student can be accepted to the erasmus program!

def check_eligibility(username, universities):
    uni = []
    query = c.execute("select * from uni")
    try:
        uni = c.fetchall()
    except:
        print("error")

    print(uni)

    query = c.execute("select * from users where username='%s'" % username)

    try:
        info = c.fetchone()
        print(info)
        if info[3] == 3:
            if (info[2] > all_courses_3rd_year - 5) or ([item for item in uni if info[5:] in item]):
                print('eligible')
                
                for x in info[5:]:
                    if remaining_seats(x):
                        break
                    else:
                        continue
        
            else:   
                print('Not eligible')

        elif info[3] >= 4:
            if (info[2] > all_courses_4rd_year - 5) and ([item for item in uni if info[5:] in item]):

                for x in info[5:]:
                    if remaining_seats(x):
                        break
                    else:
                        continue

            else:   
                print('Not eligible')
        else:
            print("Not in 3+ year")
        
    except:
        print('Not fetched anything')



@app.route('/')
def home(logged = None, type_of_user = None):
    return render_template('home.html', logged = cache.get('logged'), type_of_user = cache.get('type_of_user'))


@app.route('/admin/', methods=['GET', 'POST'])
def admin(logged = None, type_of_user = None):
    if request.method == 'POST':

        try:
            print(request.form['insert'])
        except:

            print('error')

        return 'taskte'
        
    else:
        return render_template('admin.html', logged = cache.get('logged'), type_of_user = cache.get('type_of_user'))


@app.route('/about/')
def about(logged = None, type_of_user = None):
    return render_template('about.html', logged = cache.get('logged'), type_of_user = cache.get('type_of_user'))

@app.route('/logout/')
def logout(msg = None):
    if cache.get('logged'):
        cache.set('logged', False)
        return render_template('home.html', msg = "You successfully logged out")
    else:
        msg = "You are not logged in"
        return render_template('login.html', msg = msg)

@app.route('/create_request/', methods=['GET','POST'])
def create_request(logged = None, universities = None, type_of_user = None):
    if request.method == 'POST':
        try:
            universities = [request.form['uni1'], request.form['uni2'], request.form['uni3']]
            print(universities)
            username = cache.get('username')
            print(username)
            check_eligibility(username, universities)

        except:
            print('Not found')
              
        return render_template('create_request.html', logged = cache.get('logged'), type_of_user = cache.get('type_of_user'))

    else:

        return render_template('create_request.html', logged = cache.get('logged'), type_of_user = cache.get('type_of_user'))
        

@app.route('/update_available_unis/', methods=['GET', 'POST'])
def update_available_unis(logged= None, type_of_user = None):
    if request.method == 'POST':
        try:
            name        = request.form['name']
            acceptances = request.form['acceptances']
            language    = request.form['language']
            uni = (name, acceptances, language)
            query = c.execute('insert into uni values(?, ?, ?)', uni)
            conn.commit()

        except:
            print("error updating unis") 
        finally:
            return render_template('update_available_unis.html', logged = cache.get('logged'), type_of_user = cache.get('type_of_user'))
                

    else:
        return render_template('update_available_unis.html', logged = cache.get('logged'), type_of_user = cache.get('type_of_user'))

    
@app.route('/login/', methods=['GET', 'POST'])
def login(username=None, password=None, query=None, msg=None, logged = None, type_of_user = None):
    # Login Logic 
    if request.method == 'POST':

        query = c.execute("select username, type_of_user from users where username='%s'" % request.form['username'])

        # Tries to fetch both username and pass from db and checks them
        try:
            i = c.fetchone()
            username = i[0]
            type_of_user = i[1]
            
            print(username + type_of_user)

        except TypeError:
            print('Try again')
            username = None 

        query = c.execute("select password from users where username='%s'" % request.form['username'])

        try:
           i = c.fetchone()
           password = i[0]
           print(password)

        except TypeError:
            print('Try again')
            password = None 

        if username != request.form['username'] or password != request.form['password']:
            return render_template('login.html', query = True )

        else:
            rv = cache.set('logged', True)
            usr = cache.set('username', username)
            tou = cache.set('type_of_user', type_of_user) #type of user
            return render_template('home.html', username = username, logged = rv, type_of_user = type_of_user)

    elif request.method == "GET":
        if cache.get('logged'):
            msg = "You are already logged in" 
            return render_template('login.html', msg=msg)
        else:
            return render_template('login.html') 

@app.route('/manage/')
def manage(logged = None):
    if cache.get('logged'):
        return render_template('manage.html', logged = cache.get('logged'))
    else:
        msg = "You are not logged in"
        return render_template('login.html', msg=msg)

if __name__ == '__main__':
    app.run(debug=True)
