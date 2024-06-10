import streamlit as st
import hmac # Used in the authentication
from streamlit.logger import get_logger
import pymongo
#from pymongo import MongoClient
#from pymongo.server_api import ServerApi

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="⚖️",
    )

if __name__ == "__main__":
    run()

# Authentication
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Введи код доступу", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Неправильний код доступу!")
    return False

if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Connect to Database
@st.cache_resource
def init_connection():
    client = pymongo.MongoClient(**st.secrets["mongo"])
    return client.ltg_db.pm_tlg

client = init_connection()

# def connect_ltg_db():
#     db = pymongo.MongoClient(
#         st.secrets["mongo"]["ltg_db_url"], 
#         server_api=ServerApi('1')).get_database('ltg_db')
#     return db.mycases, db.docs
    
# mycases, docs_cln = connect_ltg_db()

# @st.cache_data(ttl=600)
# def get_data():
#     db = client.mydb
#     items = db.mycollection.find()
#     items = list(items)  # make hashable for st.cache_data
#     return items

# items = get_data()

# @st.cache_data(ttl=600)
# def get_data():
#     db = client.ltg_db
#     items = db.pm_ltg
#     items = list(items)  # make hashable for st.cache_data
#     return items

# items = get_data()

# Main Streamlit app starts here

st.markdown(
    """
    ### Обери потрібний розділ:
    📊 [Аналітика](https://litigation.streamlit.app/Analytics)
    📅 [Графік засідань](https://litigation.streamlit.app/Grafic)
    ⚖️ [Судові рішення](https://litigation.streamlit.app/LTG)
    💰 [Виконавчі провадження](https://litigation.streamlit.app/VP)
"""
)

print(client.find_one({}))
