from flask import Flask, render_template, url_for, request #gets the package, imports the Flask module, render_template from the Flask package and the request feature(?)
import psycopg2
import psycopg2.extras

app = Flask(__name__) #defining the variable to use Flask with

#Database details for form data. Putting it all into a dictionary instead of an array
DB_USER = { 
  "database": "userOnboardingProject",
  "user": "postgres",
  "password": "TestTestTest1",
  "host": "db",
  "port": "5432"
}

#Checks if the table exists. If not, create it.
def create_table():
  conn = psycopg2.connect(**DB_USER)
  cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS users
    (
      customerid SERIAL PRIMARY KEY,
      firstname character(64),
      secondname character(64),
      groupid bigint,
      comment character(64)
    )
  """)
  conn.commit()

#Default endpoint
@app.route("/", methods=["GET", "POST"]) 
def index(): #ties to the main webpage for the project
  rows = []
  
  firstName = request.form.get("firstName")   #default value if the value from the user is empty is "None"
  secondName = request.form.get("secondName")
  customerID = request.form.get("customerID", type=int, default = None)
  groupID = request.form.get("groupID", type=int)
  comment = request.form.get("comment")

  
  
  if request.method == "POST": #if the HTML-request is POST
    conn = psycopg2.connect(**DB_USER) #the double stars unpacks the dictionary. Cool, right?
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    if customerID is None:
      cursor.execute("""
      INSERT INTO
        users
          (firstName, secondName, groupID, comment)
        VALUES
          (%s, %s, %s, %s)
        RETURNING *""",
          (firstName, secondName, groupID, comment)
    )
    else:
      cursor.execute("""
        INSERT INTO
          users
            (firstName, secondName, customerID, groupID, comment)
          VALUES
            (%s, %s, %s, %s, %s)
          RETURNING *""",
            (firstName, secondName, customerID, groupID, comment)
      )
    conn.commit()
    rows.append(cursor.fetchone())
    
    cursor.close()
  


  return render_template("main.html", rows=rows)

@app.route("/allusers", methods=["GET"]) #This endpoint is for listing all the users in a list
def allusers():
  limit = 10
  page = request.args.get("page", default=0, type=int)
  sortby = request.args.get("sortby", default="customerid", type=str)
  
  rows = [] #Empty array
  conn = psycopg2.connect(**DB_USER) #the double stars unpacks the dictionary. Cool, right?
  cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

  cursor.execute("""
    SELECT
      *
    FROM
      users
    ORDER BY %s
    LIMIT %d
    OFFSET %d
  """ % (sortby, limit, limit*page))
  rows = cursor.fetchall()

  cursor.close()
  
  return render_template("all-users.html", rows=rows, pagenum=page)


@app.route("/search", methods=["GET"])
def search():
  
  limit = 10
  conn = psycopg2.connect(**DB_USER)
  cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
  page = request.args.get("page", default=0, type=int) 
  search = request.args.get("search", default=0, type=str)
  rows = [] 
  pagenum = 0
  
  def empty_rows(rows):
    if len(str(search)) == 0:
      rows = [{"firstname":"No results", "secondname":"No results", 
               "customerid":"No results", "groupid":"No results", 
               "comment":"No results"}] # If the result is empty, use this instead
    return rows        


#I need to refactor this whole section with functions. 
  if search != None and len(str(search)) != 0: # Adding the string wrapping around search will prevent an exception when checking the length of an int  

    try:
      type(int(search)) # if it's convertible to an int, set it as an int for the condition checking,
      search = int(search)
    except:
      print(search)

    if isinstance(search, int): # a conditional statement with == or IS, will cause the condition check to fail
                      # Use isinstance to do a condition check on the content of the variable instead.
      cursor.execute("""
        SELECT
          *
        FROM
          users
        WHERE
          customerid = '%d'
          OR groupid = '%d'
        LIMIT %d
        OFFSET %d
      """ % (search, search, limit, limit*page))
      rows = cursor.fetchall()
      rows = empty_rows(rows)

    elif isinstance(search, str): #checking if search is an instance of a string
      cursor.execute("""
        SELECT
          *
        FROM
          users
        WHERE
          firstname LIKE ('%s%%') 
          OR secondname LIKE ('%s%%')
          OR comment LIKE ('%s%%')
        LIMIT %d
        OFFSET %d
      """ % (search, search, search, limit, limit*page)) # We need to pass two % in the query to make the interpreter think "ohh, you actually want a % here"
      rows = cursor.fetchall()
      empty_rows(rows)
    else: 
      rows = [{"firstname":"invalid search", "secondname":"invalid search", 
              "customerid":"invalid search", "groupid":"invalid search", 
              "comment":"invalid search"}]
 
  else:
    rows = empty_rows(rows)

  return render_template("search.html", rows=rows, pagenum=page)


def main():

  create_table()

  @app.after_request
  def after_request(r):
    r.headers["Cache-Control"] = "no-store" #Prevents the system from caching the HTML+CSS-files
    return r

  app.run(debug=True, host="0.0.0.0", port=8080) # Makes the application bind the webservice to localhost only.
  

if __name__ == "__main__":
  main()
