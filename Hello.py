import streamlit as st
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


if __name__ == "__main__":
    run()
