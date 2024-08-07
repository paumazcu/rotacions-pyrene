import tools
import streamlit as st
from streamlit_float import *


def get_names():
    """
    Pregunta a l'usuari quin torn correspon i quins monitors hi ha a cada camp.

    :return: (monitors_dict): diccionari amb els noms dels monitors separats per camp
    """

    common_groups =["Av Cabirols", "Av Isards", "Bold Adv", "Wild Adv"]
    global groups

    groups = {1: common_groups + ["Bike jr", "Equitació avançat"],
              2: common_groups + ["Equitació iniciació"],
              3: common_groups + ["Equitació avançat"],
              4: common_groups + ["Big Bike", "Travessa", "Equitació iniciació"],
              5: common_groups + ["Bike jr", "Travessa", "Equitació avançat"],
              6: common_groups + ["Equitació iniciació"]}

    monitors_dict = {}

    # PER FER PROVES
    # monitors_dict = {"Av Cabirols": ["Eva", "Pau"], "Av Isards": ["Blanca", "Erola"],
    #                       "Bold Adv": ["Laia", "Júlia", "Noa"], "Wild Adv": ["Vinyet", "Max", "Lara"],
    #                       "Equitació avançat": ["Manel", "Irene"], "Travessa": ["Guillem", "Èlia", "Mariona"]}

    global week_num
    # week_num = 2
    week_num = st.number_input("Introdueix el número de torn:", value=None, min_value=1, max_value=6, step=1)
    if week_num:
        st.subheader("Rotacions monis")
        st.write("Introdueix els noms dels monitors de cada camp separats per comes:")
        for group_name in groups[week_num]:
            names = st.text_input(f"{group_name}").split(",")
            monitors_dict[group_name] = [name.strip() for name in names]

    return monitors_dict


def get_groups():

    groups_dict = {}
    if week_num:
        st.subheader("Rotacions nens")
        st.write("Introdueix el número de grups que hi ha a cada camp")

        groups[week_num].append("Minairons")
        for group_name in groups[week_num]:
            if group_name == "Travessa": continue
            num = st.number_input(f"{group_name}", value=None, min_value=1, max_value=3, step=1)
            # num = input(f"{group_name} ")
            groups_dict[group_name] = num

    return groups_dict


def run():
    st.title("Rotacions Pyrene")
    with st.expander("DISCLAIMER", icon="ℹ️"):
        st.markdown(
            """
            Aquesta aplicació genera unes rotacions aleatòries per les tasques dels monitors i dels nens seguint
            les següents premises:
            - Per equilibrar les tasques entre monitors, pot haver-hi diferència entre tots els monitors com a màxim:
                * 1 Àpat
                * 1 Àpat + Nit/Despertar
                * 2 Tasques en total
            - Tant monis com nens no poden parar taula (ni despertar/nit/temps lliure en el cas de monis) si són fora.
            - Un mateix monitor no pot despertar i fer esmorzar el mateix dia.
            - Un mateix monitor no pot fer dinar i temps lliure el mateix dia.
            - Un mateix monitor no pot fer nit i despertar a la mateixa nit.
            - Tots els monitors d'un grup no poden estar alhora fent un àpat.
            - Els monitors de travessa (si n'hi ha) només fan 1 àpat com a màxim (diumenge sopar o dimecres sopar).
            - Tots els monitors excepte de travessa tenen una nit lliure el qual vol dir que es garanteix que aquesta nit
            no fan sopar, nit, despertar ni esmorzar.
            
            PD. És poc probable però podria sortir alguna incompatibilitat puntual igual que passa quan es fan les
            rotacions manualment. Tot i així s'han fet les rotacions amb menys d'1 segon i no amb 1h com es feia abans😁  
            PD2: Es recomana descarregar la taula en versió excel per si cal fer alguna modificació a mitja setmana. 
            """)


    success = False
    attempts = 0
    max_attempts = 100

    monitors_this_week = get_names()
    while not success and attempts < max_attempts:
        attempts += 1
        try:
            table_df, nits_counts, meals_counts, tl_counts, total_counts = tools.assign_names_to_tasks(monitors_this_week)
            success = True
            st.markdown(table_df.to_html(escape=False), unsafe_allow_html=True)
            # print(table_df)
            st.write("Si vols fer alguna modificació manual pots descarregar la taula en format .xlsx (Excel) al següent enllaç:")
            tools.convert_df(table_df, "rotacions_monis")


            # print("\n NITS\n", nits_counts)
            # print("\n MEALS\n", meals_counts)
            # print("\n TL\n", tl_counts)
            # print("\n TOTALS\n", total_counts)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write("\n NITS/DESPERTAR\n", nits_counts)
            with col2:
                st.write("\n ÀPATS\n", meals_counts)
            with col3:
                st.write("\n TEMPS LLIURES\n", tl_counts)
            with col4:
                st.write("\n TOTALS\n", total_counts)

        except Exception as e:
            print(f"1st algorithm. Attempt {attempts} failed: {e}. Trying again...")

    if not success:
        print("Failed to complete the  1st algorithm after maximum attempts.")


def run2():
    num_of_groups = get_groups()

    success = False
    attempts = 0
    max_attempts = 50

    while not success and attempts < max_attempts:
        attempts += 1
        try:
            table_nens_df = tools.assign_groups_to_tasks(num_of_groups)
            st.markdown(table_nens_df.to_html(escape=False), unsafe_allow_html=True)
            st.write("Si vols fer alguna modificació manual pots descarregar la taula en format .xlsx (Excel) al següent enllaç:")
            tools.convert_df(table_nens_df, "rotacions_nens")
            success = True
        except Exception as e:
            print(f"2nd algorithm. Attempt {attempts} failed: {e}. Restarting and trying again...")

    if not success:
        print("Failed to complete the 2nd algorithm after maximum attempts for de 2nd algorithm.")


if __name__ == "__main__":
    run()
    run2()