from v1 import app
from v1.models import db

if __name__ == "__main__":
    db.create_table()
    app.run(debug=True)
    