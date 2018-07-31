from v1 import app
from v1.models import CreateTables



if __name__ =="__main__":
    db_con=CreateTables()
    db_con.create_table()
    app.run(debug=True)