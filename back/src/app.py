from app import create_app, wipe_db
from app.db_models import db
from app.db_controller import populate_database

print("""  
  _______ _______ ______ _        _____            _     _                         _ 
 |__   __|__   __|  ____| |      |  __ \          | |   | |                       | |
    | |     | |  | |__  | |      | |  | | __ _ ___| |__ | |__   ___   __ _ _ __ __| |
    | |     | |  |  __| | |      | |  | |/ _` / __| '_ \| '_ \ / _ \ / _` | '__/ _` |
    | |     | |  | |    | |____  | |__| | (_| \__ \ | | | |_) | (_) | (_| | | | (_| |
    |_|     |_|  |_|    |______| |_____/ \__,_|___/_| |_|_.__/ \___/ \__,_|_|  \__,_|                                                                                                                                                
    """)

if __name__ == '__main__':
    app = create_app()
    # wipe_db(db)
    # populate_database()
    app.run(use_reloader=False)
