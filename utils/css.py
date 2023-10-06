import streamlit as st

@st.cache_data(show_spinner=False)
def hide_elements():
    hide_footer = """
                <style>
                    footer {visibility: hidden;} 
                    .viewerBadge_container__r5tak styles_viewerBadge__CvC9N {visibility: hidden;}
                    .stActionButton {visibility: hidden;}
                </style>"""
    st.write(hide_footer, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def icon_style():
    icon_style = """           
                <style>
                    .social-icons {
                        display: flex;
                        flex-wrap: wrap;
                        justify-content: space-between;
                        align-items: center;
                        max-width: 100%; /* Adjust as needed */
                        width: 100%;
                        padding: 0 10px; 
                        /* Some padding to ensure icons aren't at the very edge on small devices */
                    }

                    .icon {
                        display: block;
                        width: 25px;
                        height: 25px;
                        margin: 5px;
                        /* Adjusted margin to make it symmetrical */
                        background-size: cover;
                        background-position: center;
                        transition: transform 0.3s;
                    }

                    .icon:hover {
                        transform: scale(1.1);
                    }

                    .viewit {
                        background-image: url('https://viewit.ae/_nuxt/img/viewit-logo-no-text.25ba9bc.png');
                    }

                    /* .github {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Github-1024.png');
                    } */

                    .facebook {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Facebook-1024.png');
                    }

                    .mail { /* https://cdn4.iconfinder.com/data/icons/essentials-74/24/001_-_Envelope-1024.png */
                        background-image: url('https://cdn2.iconfinder.com/data/icons/buno-ui-interface/32/__email_mail-1024.png');
                    }

                    .twitter { /* https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Twitter-1024.png */
                        background-image: url('https://cdn0.iconfinder.com/data/icons/significon-social/512/Significon-Twitter-1024.png');
                    }

                    .instagram {
                        background-image: url('https://cdn2.iconfinder.com/data/icons/social-icons-33/128/Instagram-1024.png');
                    }
                    .css-1r6slb0, .e1f1d6gn1 {
                        display: flex;
                        justify-content: center; /* Horizontal centering */
                    }
                </style>
                """

    st.markdown(icon_style, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def chatbox_color(ai_color: str = "rgba(0,0,0,0)", user_color: str = "rgba(240, 242, 246, 0.5)"):
    """Change the background color of the chat message.
    Use css supported codes, and use hex code with the `#` symbol."""
    
    chat_css = f"""
    <style>
        .css-4oy321, .st-emotion-cache-4oy321 {{
            background-color: {ai_color};
            padding: 16px 16px 16px 16px;
        }}
        .css-1c7y2kd, .st-emotion-cache-1c7y2kd {{
            background-color: {user_color};
        }}
    </style>"""
    st.write(chat_css, unsafe_allow_html=True)
