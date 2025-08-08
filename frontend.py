import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]
message_history=[]
config={'configurable':{'thread_id':'thread1'}}
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input=st.chat_input("Type something...")
if user_input:

    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # res=chatbot.invoke({'messages':[HumanMessage(content=user_input)]},config=config)
    # ai_message=res['messages'][-1].content
    # st.session_state['message_history'].append({'role':'user','content':ai_message})
    with st.chat_message('ai'):
       ai_message= st.write_stream(
            message.content for message,metadata  in chatbot.stream(
                 {'messages':[HumanMessage(content=user_input)]},
                 config=config,
                 stream_mode="messages"
            )
        )
       st.session_state['message_history'].append({'role':'user','content':ai_message})
       
    
