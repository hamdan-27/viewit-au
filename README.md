# ViewIt Chatbot - for Pakistan

_The complete AI real estate agent, and more._

![ViewIt.AI Logo](https://i.postimg.cc/Nfz5nZ8G/Logo.png)

---

_It is recommmended to create a virtual environment and install the requirements specified in the `requirements.txt` file:_

    $ pip3 install -r requirements.txt

---
### 1. `main.py`

For debugging:

Runs the chatbot on the streamlit interface. Simply navigate to this directory on your cli and run:

    $ streamlit run Chat.py


## Live app:

[Open In Streamlit](https://viewit-ai-pk.streamlit.app/)

[Official Streamlit Documentation](https://docs.streamlit.io/)

---
### 2. `terminal_chatbot.py`

Runs the QA feature on the jupyter notebook. Reads the DataFrame from CSV and defines the question answering function.

Simply call the `agent.run()` method and pass the question to generate responses.