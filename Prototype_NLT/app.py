from Components.Call_API import Call_GPT
import streamlit as st
from time import time, sleep
from Database.mongodb import insert_in_database, get_database, close_connection

st.title("Prototype Chat_GPT")

name = st.text_input(label= 'Nom',label_visibility='hidden',placeholder=f"Entrez votre nom")
Prompt = st.text_area(label= 'prompt',label_visibility='hidden',placeholder=f"Décris-moi la fonction Python souhaitée :")

if 'prompted' not in st.session_state:
    st.session_state.prompted = False

def click_prompt():
    st.session_state.prompted = True

cols_up1, cols_up2 = st.columns([3,1])

def reset_prompt():
    st.session_state.prompted = False

#Caching API Call
@st.cache_data
def Call(Input):
    output = Call_GPT(Input)
    return output

with cols_up2:
    bip = st.button(label="Generate", on_click=click_prompt, disabled=st.session_state.prompted)

#splitting bottom of page
cols_bot1, cols_bot2 = st.columns(2)



if bip:
    heure = time()
    ret = Call(Prompt)
    duree = round((time() - heure), 2)
    st.write(f" Le résultat a mis {duree} secondes à être généré")
    insert_in_database(Prompt, ret, name)
    sessions, client = get_database(name)
    close_connection(client)
    with cols_bot1:
        Output = st.text_area(label='AI Output', value=ret)
    with cols_bot2:
        st.markdown(Output)
    with cols_up2:
        st.button(label='Prompt Again', on_click=reset_prompt, disabled=not st.session_state.prompted)

        
#Declaring a sidebar with session History

with st.sidebar:
    st.subheader('Sessions')
    st.button('Debug', on_click=reset_prompt)

<<<<<<< HEAD
if st.button(label="Generate"):
    heure = time()
    ret = Call_GPT(Prompt)
    st.write(ret)
    duree = round((time() - heure), 2)
    st.write(f" Le résultat a mis {duree} secondes à être généré")
    insert_in_database(Prompt, ret, name)
    sessions, client = get_database(name)
    for session in sessions:
        st.markdown(f"Username: {session['username']}<br>Prompt: {session['prompt']}<br>Result: {session['result']}", unsafe_allow_html=True)
    close_connection(client)
=======
>>>>>>> 92ddffe25c9730a230dca831781420dd0c300770
