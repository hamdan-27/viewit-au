import utils.agents as agents
from utils.prompts import *
from utils import css

import streamlit as st
from datetime import datetime
import os, uuid, time, openai, random

from trubrics.integrations.streamlit import FeedbackCollector
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
from langchain.callbacks import get_openai_callback
# from langchain.schema.messages import HumanMessage, AIMessage
# from langchain.agents import create_pandas_dataframe_agent

# Set page launch configurations
try:
    st.set_page_config(
        page_title="Viewit-AI.AU | Property Analyst", page_icon="🏠",
        initial_sidebar_state='auto',
        menu_items={'Report a bug': 'https://viewit-ai-au.streamlit.app/feedback',
                    'About': """### Made by ViewIt
Visit us: https://viewitproperty.com.au

Join the ViewIt.AI waitlist: https://viewit.ai

© 2023 ViewIt. All rights reserved."""})

except Exception as e:
    st.toast(str(e))
    st.toast("Psst. Try refreshing the page.", icon="👀")


@st.cache_data(show_spinner=False)
def init_trubrics(project='default', email=st.secrets.TRUBRICS_EMAIL, password=st.secrets.TRUBRICS_PASSWORD):
    """Initialize Trubrics FeedbackCollector"""
    collector = FeedbackCollector(
        project=project,  # TODO: change to viewit-ae before deployment
        email=email,
        password=password
    )
    return collector



collector = init_trubrics(project='viewit-au')

# Add session state variables
if "prompt_ids" not in st.session_state:
    st.session_state["prompt_ids"] = []
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())


# if 'button_question' not in st.session_state:
#     st.session_state['button_question'] = ""
# if 'disabled' not in st.session_state:
#     st.session_state['disabled'] = False


# VARIABLES
TEMPERATURE = 0.1
df = agents.load_data('au_new.csv')
model = 'gpt-4'

llm = ChatOpenAI(temperature=TEMPERATURE,
                 model_name=model,
                 openai_api_key=st.secrets['api_key'])

# llm = AzureChatOpenAI(
#     verbose=True,
#     temperature=TEMPERATURE,
#     openai_api_key=st.secrets['azure_key'],
#     openai_api_type = "azure",
#     openai_api_base = "https://viewit-ai.openai.azure.com/",
#     openai_api_version = "2023-07-01-preview",
#     deployment_name="Hamdan_16K"
# )

spinner_texts = [
    '🧠 Thinking...',
    '📈 Performing Analysis...',
    '👾 Contacting the hivemind...',
    '🏠 Asking my neighbor...',
    '🍳 Preparing your answer...',
    '🏢 Counting buildings...',
    '👨 Pretending to be human...',
    '👽 Becoming sentient...',
    '🔍 Finding your property...'
]

# API keys
if type(llm) == ChatOpenAI:
    openai.api_type = "open_ai"
    openai.api_base = "https://api.openai.com/v1"
    openai.api_key = st.secrets["api_key"]
    openai.organization = st.secrets["org"]
    openai.api_version = None
openai.api_key = st.secrets['api_key']
os.environ["GPLACES_API_KEY"] = st.secrets['gplaces_key']


# APP INTERFACE START #

# Add Viewit logo image to the center of page
col1, col2, col3 = st.columns(3)
with col2:
    st.image("imgs/Viewit ai Logo.png", width=200)


# App Title
st.header('ViewIt-AI.AU • Your Reliable Virtual Agent')
st.text('Thousands of properties. One AI. More than an agent.')


# AGENT CREATION HAPPENS HERE
agent = agents.create_pandas_dataframe_agent(
    llm=llm,
    df=df,
    prefix=REIDIN_PREFIX,
    suffix=SUFFIX,
    # format_instructions=FORMAT_INSTRUCTIONS,
    verbose=True,
    handle_parsing_errors=True
)

# Show data that is being used
with st.expander("Show data"):
    # add simple password for data access
    data_container = st.empty()
    data_pwd = data_container.text_input(
        "Enter password to access data", type='password')
    if data_pwd == "viewitisthebest":
        data_container.empty()
        st.write(f"Total rows: {len(df)}")
        st.dataframe(df)
    elif data_pwd == "":
        pass
    else:
        st.warning("Wrong password!")


# App Sidebar
with st.sidebar:
    # st.write("session state msgs: ", st.session_state.langchain_messages)
    # st.write("StreamlitChatMessageHistory: ", msgs.messages)

    # Description
    st.markdown("""
                # About
                Introducing ViewIt.AI, a Real Estate Chatbot Assistant that can 
                assist you with all your real estate queries 🤖

                # Data
                Uses an open source property data source currently limited to 
                Northern Territory (NT) of Australia.

                Source: 
                [Australian Housing Prices | Kaggle](https://kaggle.com/datasets/thedevastator/australian-housing-data-1000-properties-sampled/)
                """)

    st.write('---')
    st.write(f'''
    <div class="social-icons">
        <a href="https://viewitproperty.com.au" class="icon viewit" aria-label="ViewIt"></a>
        <a href="mailto:farhan@viewit.ae" class="icon mail" aria-label="Mail"></a>
        <!-- <a href="https://facebook.com/viewit.au" class="icon facebook" aria-label="Facebook"></a> -->
        <!-- <a href="https://instagram.com/viewit.pk" class="icon instagram" aria-label="Instagram"></a> -->
        <a href="https://twitter.com/aeviewit" class="icon twitter" aria-label="Twitter"></a>
    </div>''', unsafe_allow_html=True)
    st.write('---')

    # with st.expander("Commonly asked questions"):
    #     st.info(""" """)

    st.caption("© Made by ViewIt 2023. All rights reserved.")
    st.caption('''By using this chatbot, you agree that the chatbot is provided on 
            an "as is" basis and that we do not assume any liability for any 
            errors, omissions or other issues that may arise from your use of 
            the chatbot.''')


# Suggested questions
# questions = [
#     'What is the closest supermarket to the cheapest property in Dubai Marina?',
#     'What is the most recent transaction in Fairways North?',
#     'Is JLT closer to Sharjah than Arabian Ranches?'
# ]


# def send_button_ques(question):
#     st.session_state.disabled = True
#     st.session_state['button_question'] = question

# Welcome message
welcome_msg = "G'day mate, welcome to ViewIt! I'm your virtual assistant. How can I help you today?"
if "messages" not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", "content": welcome_msg}]

# if len(msgs.messages) == 0:
#     msgs.add_ai_message(welcome_msg)

# bot_avatar = "imgs/mascot_crop.png"
# bot_avatar = "https://viewit.ae/_nuxt/img/viewit-logo-no-text.25ba9bc.png"
# bot_avatar = "imgs/viewit-logo-expanded.png"
bot_avatar = "imgs/viewit-blue-on-white.png"
# bot_avatar = "imgs/viewit-white-on-blue.png"

feedback = None
# Render current messages from StreamlitChatMessageHistory
for n, msg in enumerate(st.session_state.messages):
    if msg["role"] == "assistant":
        st.chat_message(msg["role"], avatar=bot_avatar).write(msg["content"])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

# for n, msg in enumerate(msgs.messages):
#     st.chat_message(msg.type).write(msg.content)

    # Render suggested question buttons
    # buttons = st.container()
    # if n == 0:
    #     for q in questions:
    #         button_ques = buttons.button(
    #             label=q, on_click=send_button_ques, args=[q],
    #             disabled=st.session_state.disabled
    #         )
    user_query = ""
    # if msg.type == 'user':
    #     user_query = msg.content
    if msg["role"] == 'user':
        user_query = msg["content"]

    # Add feedback component for every AI response
    # if msg.type == 'assistant' and msg.content != welcome_msg:
    if msg["role"] == 'assistant' and msg["content"] != welcome_msg:
        feedback = collector.st_feedback(
            component="chat-response",
            feedback_type="thumbs",
            model=model,
            tags=['viewit-au'],
            metadata={'query': user_query, 'ai-response': msg["content"]},
            user_id=None,
            open_feedback_label="How do you feel about this response?",
            align="flex-end",
            key=f"feedback_{int(n/2)}"
        )

# Maximum allowed messages
max_messages = (
    21  # Counting both user and assistant messages including the welcome message,
        # so 10 iterations of conversation
)

# Display modal and prevent usage after limit hit
# if len(msgs.messages) >= max_messages:
if len(st.session_state.messages) >= max_messages:
    st.info(
        """**Notice:** The maximum message limit for this demo version has been reached. 
        We value your interest! Like what we're building? Please create 
        an account to continue using, or check our available pricing plans 
        [here](https://viewit.ai/)."""
    )
    # TODO: Add HubSpot form if needed

else:
    # If user inputs a new prompt or clicks button, generate and draw a new response
    if user_input := st.chat_input('Ask away'):
    # or st.session_state['button_question']:

        # Write user input
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # Log user input to terminal
        user_log = f"\nUser [{datetime.now().strftime('%H:%M:%S')}]: " + \
            user_input
        print('='*90)
        print(user_log)

        # Note: new messages are saved to history automatically by Langchain during run
        with st.spinner(random.choice(spinner_texts)):
            css.icon_style()
            css.hide_elements()
            css.ai_chatbox_style()
            try:
                # Get token usage info with openai callback
                with get_openai_callback() as cb:
                    response = agent.run(user_input)
                    print(cb)

            # Handle the parsing error by omitting error from response
            except Exception as e:
                response = str(e)
                if response.startswith("Could not parse LLM output: `"):
                    response = response.removeprefix(
                        "Could not parse LLM output: `").removesuffix("`")
                st.toast(str(e), icon='⚠️')
                print(str(e))

        # Clear button question session state to prevent answer regeneration on rerun
        # st.session_state['button_question'] = ""

        # Write AI response
        with st.chat_message("assistant", avatar=bot_avatar):
            st.session_state.messages.append({"role": "assistant", "content": response})
            message_placeholder = st.empty()
            full_response = ""

            # Simulate stream of response with milliseconds delay
            for chunk in response.split(' '):
                full_response += chunk + " "
                time.sleep(0.02)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)

        logged_prompt = collector.log_prompt(
            config_model={"model": model, 'temperature': TEMPERATURE},
            prompt=user_input,
            generation=response,
            session_id=st.session_state.session_id,
            tags=['viewit-au']
        )
        st.session_state.prompt_ids.append(logged_prompt.id)

        # Log AI response to terminal
        response_log = f"Bot [{datetime.now().strftime('%H:%M:%S')}]: " + \
            response
        print(response_log)
        # st.experimental_rerun()

if len(st.session_state.messages) == 3:
    st.toast("Tip: Press `R` to refresh the app.", icon="ℹ️")

# CSS for social icons
css.icon_style()
css.hide_elements()
css.ai_chatbox_style()