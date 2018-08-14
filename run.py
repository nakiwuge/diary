from v1 import app
from v1.models import db


#app.config.from_object(all_configs['develop'])
''' running the app'''
if __name__ =="__main__":
    app.run(debug=True)
    db.create_table()
    