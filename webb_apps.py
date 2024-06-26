# importation des modules
import streamlit as st 
import requests
import pandas as pd

# Intro
st.title('Récupération Videos :blue[cool] :sunglasses:')

st.subheader('Récupération des liens des videos du site video', divider='rainbow')
lien = st.text_input('Lien', placeholder='Insérez le lien de la vidéo')

# Chargement des liens des videos 
def get_url_video(lien):
    #url = 'https://mybollyfrench.com/playlist/mehndi-hai-rachne-wali/'
    base = 'https://mybollyfrench.com/playlist/'
    objet = lien.replace(base,'')
    url_api = f'https://mybollyfrench.com/api/public/websites/v1/items/{objet}'
    r = requests.get(url_api)
    contenu = r.json()
    return contenu

def get_link(lien):
    contenu = get_url_video(lien)
    nombre_episodes = len(contenu['content_object']['medias'])
    nom_episode = contenu['content_object']['medias'][0]['name']
    nombre_episodes = len(contenu['content_object']['medias'])
    sortie = pd.DataFrame()
    j = 0
    for i in range(nombre_episodes):
        sortie.at[j,'episode'] = contenu['content_object']['medias'][i]['name']
        sortie.at[j,'Fichier'] = contenu['content_object']['medias'][i]['src']
        sortie.at[j, 'Taille'] = contenu['content_object']['medias'][i]['duration']
        j += 1
    return sortie

def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
    )
    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

    # Evenement de clic
if lien:
    tableau = get_link(lien)
    #df = st.dataframe(tableau,column_config={'playlist':st.column_config.LinkColumn('playlist'),'Fichier':st.column_config.LinkColumn('Fichier')})
    #st.dataframe(df)
    #md = tableau.to_html(render_links=True)
    #st.markdown(md,unsafe_allow_html=True)
    selection = dataframe_with_selections(tableau)
    st.subheader('Lecture en video', divider='rainbow')
    try :
        st.video(selection['Fichier'].values[0])
    except IndexError:
        pass
