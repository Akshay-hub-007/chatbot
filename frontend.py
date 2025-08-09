import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

def generate_uuid():
    thread_id=uuid.uuid4()

    return thread_id

def reset_chat():
    thread_id=generate_uuid()
    st.session_state['thread_id']=thread_id
    add_thred(st.session_state['thread_id'])
    st.session_state['message_history']=[]

def add_thred(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable':{'thread_id':st.session_state['thread_id']}}).values['messages']

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=  generate_uuid()
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

add_thred(st.session_state['thread_id'])

message_history=[]

st.sidebar.title('LangGraph chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.header('My Conversations')
for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages



config={'configurable':{'thread_id':st.session_state['thread_id']}}
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
       
    
