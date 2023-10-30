import streamlit as st
import hmac # Used in the authentication
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="⚖️",
    )

    st.write("# Hello! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        **👈 Для початку роботи введи код доступу**
        ### Потім обери розділ, який тебе цікавить:
        - Аналітика [Analytics](https://litigation.streamlit.app/Analytics)
        - Графік засідань [Grafic](https://litigation.streamlit.app/Grafic)
        - Судові справи [LTG](https://litigation.streamlit.app/LTG)
        - Виконавчі провадження [VP](https://litigation.streamlit.app/VP)
    """
    )

# Authentication
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["test"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the passward is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect!")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

# Main Streamlit app starts here
st.write("Here goes your normal Streamlit app...")
st.button("Click me")

if __name__ == "__main__":
    run()
