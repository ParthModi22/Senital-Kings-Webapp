import streamlit as st
# from statics.sidebar_style import add_custom_css

def sidebar_navigation():
    # add_custom_css()
    
    col1, col2, col3 = st.sidebar.columns([1,8,1])
    with col1:
        st.write("")
    with col2:
        st.image('statics/logo4.png',  use_column_width=True)
    with col3:
        st.write("")
    # st.sidebar.markdown(
    #     "<div style='text-align: center; font-size:24px; font-weight:bold;'>SENTINAL KINGS</div>",
    #     unsafe_allow_html=True
    # )
    st.sidebar.title("Navigation")
    # st.markdown(
    #     """
    #     <h2 style='text-align: center; font-size: 40px'>
    #         Navigation
    #     </h2>
    #     """,
    #     unsafe_allow_html=True
    # )
    # Create sidebar navigation options
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["Introduction","Irrigation Monitoring"]  # Unified Farm Maps section
    )
    return page
