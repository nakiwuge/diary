from v1 import app
from v1.models import User



if __name__ =="__main__":
    db_con=User()
    db_con.create_tables()
    app.run(debug=True)