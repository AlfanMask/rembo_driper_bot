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
from constants import lang, input_state, numbers, notif, premium_type, ai_assistant_mode

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
    
    # USERS namepsace
    class users:
        def __init__(self):
            self = self
            
        # GET (read) namespace
        class get:
            def __init__(self):
                self = self
                
            def lang_by_user_id(user_id: str) -> lang:
                conn = db.connect()
                cursor = conn.cursor()
                
                # get lang
                cursor.execute(f"SELECT lang FROM users WHERE user_id = '{user_id}'")
                user_lang: lang = cursor.fetchone()

                if user_lang:
                    return user_lang[0]
                return None
            
            def active_preference_ai(user_id:str) -> str:
                conn = db.connect()
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT preference_ai FROM users WHERE user_id = '{user_id}'")
                result = cursor.fetchone()

                return result[0]

            def input_state_by_user_id(user_id: str) -> str:
                conn = db.connect()
                cursor = conn.cursor()
                
                # get input_state
                cursor.execute(f"SELECT input_state FROM users WHERE user_id = '{user_id}'")
                input_state: str = cursor.fetchone()
                
                if input_state:
                    return input_state[0]
                return None
            
            def ai_mode_by_user_id(user_id:str) -> str:
                conn = db.connect()
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT ai_mode FROM users WHERE user_id = '{user_id}'")
                result = cursor.fetchone()

                return result[0]
            
        # UPDATE namespace
        class update:
            def __init__(self):
                self = self

            def input_state_by_user_id(user_id: str, state: str) -> None:
                conn = db.connect()
                cursor = conn.cursor()
                
                # update input_state
                cursor.execute(f"UPDATE users SET input_state = '{state}' WHERE user_id = '{user_id}'")
                
                # commit query
                conn.commit()
                conn.close()
                
            def preference_ai_by_user_id(user_id: str, pref_ai: str) -> None:
                conn = db.connect()
                cursor = conn.cursor()
                
                # update input_state
                cursor.execute(f"UPDATE users SET preference_ai = '{pref_ai}' WHERE user_id = '{user_id}'")
                
                # commit query
                conn.commit()
                conn.close()
                
            def mode_ai_by_user_id(user_id: str, ai_mode: ai_assistant_mode) -> None:
                conn = db.connect()
                cursor = conn.cursor()
                
                # update input_state
                cursor.execute(f"UPDATE users SET ai_mode = '{ai_mode}' WHERE user_id = '{user_id}'")
                
                # commit query
                conn.commit()
                conn.close()
                
                
        # DELETE namespace
        class delete:
            def __init__(self):
                self = self
                
            def input_state_by_user_id(user_id: str) -> None:
                conn = db.connect()
                cursor = conn.cursor()
                
                # delete input_state from user
                cursor.execute(f"UPDATE users SET input_state = NULL WHERE user_id = '{user_id}'")

                # commit query
                conn.commit()
                conn.close()

        
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
                
                cursor.execute(f"SELECT link, message FROM magers WHERE univ='UNS' AND type LIKE '%#ANJEM%' AND is_reminded = 0 AND num_comments IS NULL AND deleted = 0 AND is_closed = 0 AND (created_at BETWEEN NOW() - INTERVAL 1 HOUR AND NOW() - INTERVAL 5 MINUTE) ORDER BY id ASC LIMIT 1")
                result = cursor.fetchone()

                if result:
                    return (result[0], result[1])
                return (None, None)
                        
            def newest_anjem_ums_dont_get_drivers_link() -> tuple[str, str]:
                conn = db.connect()
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT link, message FROM magers WHERE univ='UMS' AND type LIKE '%#ANJEM%' AND is_reminded = 0 AND num_comments IS NULL AND deleted = 0 AND is_closed = 0 AND (created_at BETWEEN NOW() - INTERVAL 1 HOUR AND NOW() - INTERVAL 5 MINUTE) ORDER BY id ASC LIMIT 1")
                result = cursor.fetchone()

                if result:
                    return (result[0], result[1])
                return (None, None)
            
            def newest_anjem_uny_dont_get_drivers_link() -> tuple[str, str]:
                conn = db.connect()
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT link, message FROM magers WHERE univ='UNY' AND type LIKE '%#ANJEM%' AND is_reminded = 0 AND num_comments IS NULL AND deleted = 0 AND is_closed = 0 AND (created_at BETWEEN NOW() - INTERVAL 1 HOUR AND NOW() - INTERVAL 5 MINUTE) ORDER BY id ASC LIMIT 1")
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
            def new(user_id: str, message_type: str, message: str, ai_mode: ai_assistant_mode) -> bool:
                conn = db.connect()
                cursor = conn.cursor()
                
                # insert
                created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO ai_assistant_messages (user_id, type, message, mode, created_at) VALUES (%s, %s, %s, %s, %s)", (user_id, message_type, message, ai_mode, created_at))

                conn.commit()
                conn.close()
                
        # GET (read) namespace
        class get:
            def __init__(self):
                self = self
                
            # get chat context of the last 1 day so able to continue the chat with users
            def last_30_chats_from_user_id(user_id: str, ai_mode: ai_assistant_mode) -> list[str]:
                conn = db.connect()
                cursor = conn.cursor()
                
                query = "SELECT message FROM ai_assistant_messages WHERE user_id = %s AND mode = %s AND is_resetted = 0 AND (created_at BETWEEN NOW() - INTERVAL 24 HOUR AND NOW()) ORDER BY id DESC LIMIT 30"
                
                cursor.execute(query, (user_id,ai_mode,))
                result = cursor.fetchall()
                
                # Extract messages from the result and reverse the list to get the oldest first
                messages = [row[0] for row in result][::-1]
                
                cursor.close()
                conn.close()
                
                return messages
            
            
        # UPDATE namespace
        class update:
            def __init__(self):
                self = self
                
            def delete_memory_by_user_id(user_id: str) -> list[str]:
                conn = db.connect()
                cursor = conn.cursor()
                
                query = "UPDATE ai_assistant_messages SET is_resetted = 1 WHERE user_id = %s AND is_resetted = 0"
                
                cursor.execute(query, (user_id,))
                
                # commit query
                conn.commit()
                conn.close()
                
                
    # DRIVER namepsace
    class drivers:
        def __init__(self):
            self = self
                
        # GET (read) namespace
        class get:
            def __init__(self):
                self = self
                
            # check if there are >= 5 orders that dont get driver yet
            def driver_ids_of_inactive_drivers() -> bool:
                conn = db.connect()
                cursor = conn.cursor()
                
                cursor.execute(f"SELECT driver_id FROM drivers WHERE is_active = 0")
                driver_ids: list[str] = [driver[0] for driver in cursor.fetchall()]
                
                if len(driver_ids) > 0:
                    return driver_ids
                return False