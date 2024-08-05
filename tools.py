import restrictions
import random
import copy
tasques = ["despertar", "esmorzar", "dinar", "temps lliure", "sopar", "nit"]
days = ["diumenge", "dilluns", "dimarts", "dimecres", "dijous", "divendres", "dissabte"]


def createHorari():
    """
    Crea un diccionari amb els dies de la setmana de diumenge a dissabte com a keys i les tasques com a values.
    Cada tasca és un nou diccionari que té per value una tupla (número, llista buida)

    :return: (week): el diccionari principal
    """

    # cada tasca de cada dia de la setmana està associat a una parella (número, llista)
    # El número indica el nombre de gent necessària, i la llista els noms de la gent
    week = {day: {tasca: (0, []) for tasca in tasques} for day in days}

    # Actualitza els números
    # NIT
    for day in ["diumenge", "divendres"]:
        week[day]["nit"] = (3, [])
    for day in ["dilluns", "dimarts", "dimecres", "dijous"]:
        week[day]["nit"] = (2, [])

    # DESPERTAR
    for day in days[1:]:
        week[day]["despertar"] = (2, [])

    # TEMPS LLIURE
    for day in ["dilluns", "dimarts", "dijous"]:
        week[day]["temps lliure"] = (2, [])

    # ESMORZAR
    for day in ["dilluns", "dimarts", "dissabte"]:
        week[day]["esmorzar"] = (4, [])
    for day in ["dijous", "divendres"]:
        week[day]["esmorzar"] = (3, [])
    week["dimecres"]["esmorzar"] = (2, [])

    # DINAR
    for day in ["dilluns", "dimarts"]:
        week[day]["dinar"] = (3, [])
    week["dijous"]["dinar"] = (4, [])

    # SOPAR
    for day in days[1:-1]:
        week[day]["sopar"] = (4, [])
    week["diumenge"]["sopar"] = (5, [])




    return week

week = createHorari()

def get_groups():
    """
    Pregunta a l'usuari quin torn correspon i quins monitors hi ha a cada camp.

    :return: (monitors_this_week): diccionari amb els noms dels monitors separats per camp
    """

    common_groups =["Av Cabirols", "Av Isards", "Bold Adv", "Wild Adv"]

    groups = {1: common_groups + ["Bike jr", "Equitació avançat"],
              2: common_groups + ["Equitació iniciació"],
              3: common_groups + ["Equitació avançat"],
              4: common_groups + ["Big Bike", "Travessa", "Equitació iniciació"],
              5: common_groups + ["Bike jr", "Travessa", "Equitació avançat"],
              6: common_groups + ["Equitació iniciació"]}
    monitors_this_week = {}

    ########################################
    # DESCOMENTAR QUAN ES VULGUI LA VERSIÓ FINAL
    ############################################
    # week_num = int(input("Introdueix el número de la setmana: "))
    #
    # for group_name in groups[week_num]:
    #     names = input(f"Introdueix els noms dels monitors de {group_name}: separats per comes: ").split(",")
    #     monitors_this_week[group_name] = [name.strip() for name in names]

    monitors_this_week = {"Av Cabirols": ["Eva", "Pau"], "Av Isards": ["Blanca", "Erola"],
                          "Bold Adv": ["Laia", "Júlia", "Noa"], "Wild Adv": ["Vinyet", "Max", "Lara"],
                          "Travessa": ["Guillem", "Èlia", "Mariona"], "Equitació avançat": ["Manel", "Irene"]}
    return monitors_this_week


def can_assign(group, moni, day, task):
    """
    Comprova si pot assignar monitors d'un camp a una tasca
    :param group: nom del camp
    :param day: dia
    :param task:
    :return: boolean si es pot assignar o incompleix alguna restricció
    """

    # Restriccions de camp
    restriction_key = f"{day}_{task}"
    if restriction_key in restrictions.restriccions and group in restrictions.restriccions[restriction_key]:
        return False

    for i, d in enumerate(days):
        if d == day:
            yesterday = days[i-1]
            break

    # Incompatibilitats de tasques
    if task == "esmorzar" and moni in week[day]["despertar"][1]:
        return False
    elif task == "temps lliure" and moni in week[day]["dinar"][1]:
        return False
    elif task == "despertar" and moni in week[yesterday]["nit"][1]:
        return False
    return True

def find_group_by_monitor(dictionary, monitor):
    """
    Obtenir el grup donat un nom d'un monitor
    :return: el nom del grup
    """
    for key, values in dictionary.items():
        if monitor in values:
            return key
    return None  # Return None if the value is not found

def assign_names_to_tasks():

    monitors_this_week = get_groups()
    monitors_list = sum(list(monitors_this_week.values()), [])  # llista plana de tots els monitors
    meals_count_per_moni = {moni: 0 for moni in monitors_list}
    nits_desp_count_per_moni = {moni: 0 for moni in monitors_list}
    tl_count_per_moni = {moni: 0 for moni in monitors_list}
    # els anteriors diccionaris porten el recompte de les tasques que té assignades cada monitor.

    for day in week:
        for task in week[day]:
            monitors_ok = []
            monitors_not_ok = []
            limit = week[day][task][0]
            # utilitzaré la següent variable per comprovar que un grup sencer no estigui al mateix àpat
            monitors_copy = copy.deepcopy(monitors_this_week)

            while not len(monitors_ok) == limit:  # mentre no hi hagi el nombre suficient de monitors segueix buscant

                monitors_available = [x for x in monitors_list if x not in monitors_not_ok and x not in monitors_ok]

                if task in ["despertar", "nit"]:
                    nd_count_per_moni_availables = {moni: nits_desp_count_per_moni[moni] for moni in monitors_available}
                    minval = min(nd_count_per_moni_availables.values())
                    monis_with_less_nd = [k for k, v in nits_desp_count_per_moni.items()
                                          if v == minval and k in monitors_available]
                    monitor_try = random.choice(monis_with_less_nd)
                elif task in ["esmorzar", "dinar", "sopar"]:
                    meals_count_per_moni_availables = {moni: meals_count_per_moni[moni] for moni in monitors_available}
                    minval = min(meals_count_per_moni_availables.values())
                    monis_with_less_meals = [k for k, v in meals_count_per_moni.items()
                                             if v == minval and k in monitors_available]

                    monitor_try = random.choice(monis_with_less_meals)
                else:
                    minval = min(tl_count_per_moni.values())
                    monis_with_less_tl = [k for k, v in tl_count_per_moni.items()
                                          if v == minval and k in monitors_available]
                    monitor_try = random.choice(monis_with_less_tl)

                # descobreix de quin camp és el monitor que s'està provant
                group_monitor_try = find_group_by_monitor(monitors_this_week, monitor_try)

                if can_assign(group_monitor_try, monitor_try, day, task):  # comprova si incompleix alguna restricció
                    if task in ["despertar", "nit"]:
                        nits_desp_count_per_moni[monitor_try] += 1
                        monitors_ok.append(monitor_try)
                    elif task in ["esmorzar", "dinar", "sopar"]:
                        if group_monitor_try == "Travessa" and meals_count_per_moni[monitor_try] == 1:
                            monitors_not_ok.append(monitor_try)
                        else:
                            meals_count_per_moni[monitor_try] += 1
                            monitors_ok.append(monitor_try)
                            monitors_copy[group_monitor_try].remove(monitor_try)

                            # Si només queda un monitor lliure d'un camp aquest idealment ha de quedar lliure
                            if len(monitors_copy[group_monitor_try]) == 1:
                                last_moni = monitors_copy[group_monitor_try][0]
                                monitors_not_ok.append(last_moni)

                    elif task == "temps lliure":
                        tl_count_per_moni[monitor_try] += 1
                        monitors_ok.append(monitor_try)
                else:
                    monitors_not_ok.append(monitor_try)

            for moni in monitors_ok:
                week[day][task][1].append(moni)

    total_count_per_moni = {moni: nits_desp_count_per_moni[moni] +
                            meals_count_per_moni[moni] + tl_count_per_moni[moni] for moni in monitors_list}

    return week, nits_desp_count_per_moni, meals_count_per_moni, tl_count_per_moni, total_count_per_moni


prova, nits_counts, meals_counts, tl_counts, total_counts = assign_names_to_tasks()

for d in prova.items():
    print(d)

print("\n NITS\n", nits_counts)
print("\n MEALS\n", meals_counts)
print("\n TL\n", tl_counts)
print("\n TOTALS\n", total_counts)


# todo

# intentar buscar una nit lliure per tothom