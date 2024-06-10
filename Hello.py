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
    return pymongo.MongoClient(st.secrets["mongo"]["ltg_db"])

mongo_client = init_connection()

@st.cache_data(ttl=600)
def get_ecourt_data(input_case_num):
    #pm = mongo_client.ltg_db.pm_ltg.find_one({})
    data = mongo_client.ltg_db.ec_docs.find({'case_num' : input_case_num})
    docs = []
    for elem in data:
        text = elem.get('task_txt', "-")
        if text != "-":
            docs.append(text)
    return docs

# Main Streamlit app starts here

# st.markdown(
#     """
#     ### Обери потрібний розділ:
#     ⚖️ [Судові рішення](https://litigation.streamlit.app/LTG)\n
#     📅 [Графік засідань](https://litigation.streamlit.app/Grafic)\n
#     💰 [Виконавчі провадження](https://litigation.streamlit.app/VP)\n
#     📊 [Аналітика](https://litigation.streamlit.app/Analytics)\n
# """
# )

case_num = st.text_input("Знайти інформацію за номером справи", "Номер справи")

# options = st.multiselect(
#     "Шукати",
#     ["Рішення", "Засідання"],
#     ["Рішення", "Засідання"])


# Get the list of docs (task_text)
edocs = get_ecourt_data(case_num)

st.write(edocs)

