import os,sys, math
# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the root directory by moving up the directory tree
project_root = os.path.abspath(os.path.join(current_script_dir, ".."))

sys.path.insert(0, project_root)

from models.dataengine import Database
from instances.db import db
from uuid import uuid4 
from datetime import datetime, timedelta
from constants import lang, input_state, numbers, notif, premium_type

class Client:
    def __init__(self, db: Database):
        self.db = db
        
    # custom SELECT query
    def custom_select_query(self, query: str) -> str:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
        return str(result)

        
    # MAGER namepsace
    class magers:
        def __init__(self):
            self = self
                
        # GET (read) namespace
        class get:
            def __init__(self):
                self = self
                
            # check if there are >= 5 orders that dont get driver yet
            def is_many_orders_dont_get_driver() -> bool:
                conn = db.connect()
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT COUNT(id) FROM magers WHERE univ='UNS' AND (type LIKE '%#ANJEM%' OR type LIKE '%#JASTIP%') AND deleted = 0 AND num_comments IS NULL AND is_closed = 0 AND created_at >= NOW() - INTERVAL 1 HOUR")
                result = cursor.fetchone()

                if result[0] >= numbers.num_many_ordes_dont_get_driver:
                    return True
                return False
            
            def newest_anjem_uns_dont_get_drivers_link() -> tuple[str, str]:
                conn = db.connect()
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT link, message FROM magers WHERE univ='UNS' AND type LIKE '%#ANJEM%' AND is_reminded = 0 AND num_comments IS NULL AND deleted = 0 AND is_closed = 0 AND (created_at BETWEEN NOW() - INTERVAL 1 HOUR AND NOW() - INTERVAL 10 MINUTE) ORDER BY id ASC LIMIT 1")
                result = cursor.fetchone()

                if result:
                    return (result[0], result[1])
                return (None, None)
                        
            def newest_anjem_ums_dont_get_drivers_link() -> tuple[str, str]:
                conn = db.connect()
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT link, message FROM magers WHERE univ='UMS' AND type LIKE '%#ANJEM%' AND is_reminded = 0 AND num_comments IS NULL AND deleted = 0 AND is_closed = 0 AND (created_at BETWEEN NOW() - INTERVAL 1 HOUR AND NOW() - INTERVAL 10 MINUTE) ORDER BY id ASC LIMIT 1")
                result = cursor.fetchone()

                if result:
                    return (result[0], result[1])
                return (None, None)
            
            def newest_anjem_uny_dont_get_drivers_link() -> tuple[str, str]:
                conn = db.connect()
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT link, message FROM magers WHERE univ='UNY' AND type LIKE '%#ANJEM%' AND is_reminded = 0 AND num_comments IS NULL AND deleted = 0 AND is_closed = 0 AND (created_at BETWEEN NOW() - INTERVAL 1 HOUR AND NOW() - INTERVAL 10 MINUTE) ORDER BY id ASC LIMIT 1")
                result = cursor.fetchone()

                if result:
                    return (result[0], result[1])
                return (None, None)
    
        class update:
            def __init__(self):
                self = self
                
            def set_is_reminded_true_by_link(link: str) -> None:
                conn = db.connect()
                cursor = conn.cursor()
                
                cursor.execute(f"UPDATE magers SET is_reminded = 1 WHERE link = '{link}'")
                conn.commit()
                conn.close()
                
                
    # AI ASSISTANT MESSAGES namepsace
    class ai_assistant_messages:
        def __init__(self):
            self = self
                
        # CREATE namespace
        class create:
            def __init__(self):
                self = self
                
            # check if there are >= 5 orders that dont get driver yet
            def new(user_id: str, message_type: str, message: str) -> bool:
                conn = db.connect()
                cursor = conn.cursor()
                
                # insert
                created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO ai_assistant_messages (user_id, type, message, created_at) VALUES (%s, %s, %s, %s)", (user_id, message_type, message, created_at))

                conn.commit()
                conn.close()
                
        # GET (read) namespace
        class get:
            def __init__(self):
                self = self
                
            def last_20_chats_from_user_id(user_id: str) -> list[str]:
                conn = db.connect()
                cursor = conn.cursor()
                
                query = "SELECT message FROM ai_assistant_messages WHERE user_id = %s ORDER BY id DESC LIMIT 20"
                
                cursor.execute(query, (user_id,))
                result = cursor.fetchall()
                
                # Extract messages from the result and reverse the list to get the oldest first
                messages = [row[0] for row in result][::-1]
                
                cursor.close()
                conn.close()
                
                return messages