from Components.Call_API import call_gpt
from Components.utils_streamlit import variable_session, click_prompt, reset_prompt
import streamlit as st
from time import time
from Database.mongodb import insert_in_database, get_database, close_connection, update_database
#-----------------------------------------------Declare logics----------------------------------------
if 'prompted' not in st.session_state:
    st.session_state.prompted = False

if 'ret_output' not in st.session_state:
    st.session_state.ret_output = "init"
if 'clef' not in st.session_state:
    st.session_state.clef = "1"

with st.sidebar:
    st.subheader('Sessions')
    st.button('Debug', on_click=reset_prompt)
    name = st.text_input(label= 'Nom',label_visibility='hidden',placeholder=f"Entrez votre nom", value='Anonyme')

#Declaring a sidebar with session History
with st.sidebar: 
    sessions, client = get_database(name)
    list_session_prompt = [str(y['prompt'][:25]+'...') for y in sessions]
    list_session_prompt.insert(0, 'New_prompt...')
    sidebar_change = False
    selected_option = st.radio('Select Past Prompt', [y for y in list_session_prompt])
                            #    , on_change=onchange_sidebar)
    if selected_option != 'New_prompt...':
        selected_index = list_session_prompt.index(selected_option)
        ret_, nom, prompt_ = variable_session(selected_index, name)
        ret=ret_
        prompt = prompt_
    else:
        ret = None
        prompt = None

#-----------------------------------------------//Declare logics//----------------------------------------

#-----------------------------------------------Layout ----------------------------------------

st.title("Prototype Chat_GPT")

# # debug db
# client, collection = connection_mongodb()

# for y in collection.find():
#     st.write(y)

# def prompt_change() :
#     new_prompt = True

Prompt = st.text_area(label= 'prompt',label_visibility='hidden', value=prompt, key=2)
# , on_change= prompt_change)

cols_up1, cols_up2 = st.columns([3,1])

with cols_up2:
    bip = st.button(label="Generate", on_click=click_prompt, disabled=st.session_state.prompted)

#splitting bottom of page
cols_bot1, cols_bot2 = st.columns(2)

if bip:
    heure = time()
    ret = call_gpt(Prompt)
    duree = round((time() - heure), 2)
    st.write(f" Le résultat a mis {duree} secondes à être généré")
    insert_in_database(Prompt, ret, name)
    sessions, client = get_database(name)
    close_connection(client)

def update_Output():
    # print(st.session_state.clef)
    update_database(Prompt, ret, name, st.session_state.clef)


with cols_bot1:
    Output = st.text_area(label='AI Output', label_visibility='hidden', value=ret, key='clef', height=200, on_change=update_Output)
    
with cols_bot2:
    st.write('')
    st.write('')
    st.markdown(Output)
    
with cols_up2:
    st.button(label='Prompt Again', on_click=reset_prompt, disabled=not st.session_state.prompted)


close_connection(client)