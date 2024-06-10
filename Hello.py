import streamlit as st
import hmac # Used in the authentication
from streamlit.logger import get_logger
import pymongo
import re
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

# Functions
def clean_edoc(input_edoc):
    cleaned_edoc = input_edoc.replace('e.court@court.gov.ua', '')
    cleaned_edoc = re.sub(r'\[(.*?)\]', '', cleaned_edoc)
    return cleaned_edoc

# Connect to Database
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(st.secrets["mongo"]["ltg_db"])

mongo_client = init_connection()

@st.cache_data(ttl=600)
def get_ecourt_data(input_case_num):
    #pm = mongo_client.ltg_db.pm_ltg.find_one({})
    input_case_num = input_case_num.replace('№', '').strip()
    data = mongo_client.ltg_db.ec_docs.find({'case_num' : input_case_num})
    docs = []
    for elem in data:          
        docs.append(
            {
                'doc_title' : elem.get('doc_title', "-"),
                'doc_eid' : elem.get('doc_eid', "-"),
                'court_title' : elem.get('court_title', "-"),
                'ops_text' : elem.get('ops_txt', "-"),
                'task_text' : elem.get('task_txt', "-")
            }
        )
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

case_num = st.text_input("Знайти інформацію за номером справи", "420/8320/23")

# options = st.multiselect(
#     "Шукати",
#     ["Рішення", "Засідання"],
#     ["Рішення", "Засідання"])


# Get the list of docs (task_text)
edocs = get_ecourt_data(case_num)

for edoc in edocs:
    doc_title = edoc.get('doc_title')
    if doc_title != "-":
        st.write(f"📃[{doc_title.title()}](https://cabinet.court.gov.ua/document/{edoc.get('doc_eid')})")
    
    court_title = edoc.get('court_title')
    if court_title != "-":
        st.write(f"🏛️{court_title}")
    
    ops_text = edoc.get('ops_text')
    if doc_title != "-":
        st.write(f"👩🏻‍⚖️{ops_text}")
    
    task_text = edoc.get('task_text')
    if doc_title != "-":
        st.write(f"{clean_edoc(task_text)}")
    
    st.write("")


