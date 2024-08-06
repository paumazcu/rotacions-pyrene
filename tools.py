import restrictions
import random
import copy

tasques = ["despertar", "esmorzar", "dinar", "temps lliure", "sopar", "nit", "nit lliure"]
days = ["diumenge", "dilluns", "dimarts", "dimecres", "dijous", "divendres", "dissabte"]


def createHorari():
    """
    Crea un diccionari amb els dies de la setmana de diumenge a dissabte com a keys i les tasques com a values.
    Cada tasca és un nou diccionari que té per value una tupla (número, llista buida)

    :return: (week): el diccionari principal
    """

    # cada tasca de cada dia de la setmana està associat a una parella (número, llista)
    # El número indica el nombre de gent necessària, i la llista els noms de la gent
    empty_week = {day: {tasca: (0, []) for tasca in tasques} for day in days}

    # Actualitza els números
    # NIT
    for day in ["diumenge", "divendres"]:
        empty_week[day]["nit"] = (3, [])
    for day in ["dilluns", "dimarts", "dimecres", "dijous"]:
        empty_week[day]["nit"] = (2, [])

    # DESPERTAR
    for day in days[1:]:
        empty_week[day]["despertar"] = (2, [])

    # TEMPS LLIURE
    for day in ["dilluns", "dimarts", "dijous"]:
        empty_week[day]["temps lliure"] = (2, [])

    # ESMORZAR
    for day in ["dilluns", "dimarts", "dissabte"]:
        empty_week[day]["esmorzar"] = (4, [])
    for day in ["dijous", "divendres"]:
        empty_week[day]["esmorzar"] = (3, [])
    empty_week["dimecres"]["esmorzar"] = (2, [])

    # DINAR
    for day in ["dilluns", "dimarts"]:
        empty_week[day]["dinar"] = (3, [])
    empty_week["dijous"]["dinar"] = (4, [])

    # SOPAR
    for day in days[1:-1]:
        empty_week[day]["sopar"] = (4, [])
    empty_week["diumenge"]["sopar"] = (5, [])

    return empty_week


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


def can_assign(group, moni, day, task, nits_lliures):
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

    # Restriccions de nit lliure
    if moni in nits_lliures[day] and task in ["sopar", "nit"]:
        return False
    elif moni in nits_lliures[yesterday] and task in ["despertar", "esmorzar"]:
        return False

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

def assign_free_nights(monis_dict):
    """
    Assigna aleatoriament una nit lliure a tots els monitors.
    Nit lliure vol dir que no es fa sopar, nit, despertar ni esmorzar.
    (Travessa no entra a l'equació)
    :param monis_dict: diccionari de tots els monis separats per camps.

    :return: diccionari amb les nits lliures que té cadascú
    """

    nits_lliures = {day: [] for day in days}

    monis_sublists = [x for v, x in monis_dict.items() if v != "Travessa"]
    monis_flat = [x for li in monis_sublists for x in li]

    nits_lliures_completes = []
    for m in monis_flat:
        group = find_group_by_monitor(get_groups(), m)
        for day in days:
            if len(nits_lliures[day]) == 3:
                nits_lliures_completes.append(day)
            if group in restrictions.restriccions[f"{day}_nit fora"]:
                nit_fora = day
                break  # Només es fa màxim una nit fora
            else:
                nit_fora = None
        free_nights_available = [dia for dia in days[:-1] if dia != nit_fora and dia not in nits_lliures_completes]
        nit_lliure = random.choice(free_nights_available)
        nits_lliures[nit_lliure].append(m)

    return nits_lliures


def assign_names_to_tasks():

    global week

    week = createHorari()

    monitors_this_week = get_groups()
    monitors_list = sum(list(monitors_this_week.values()), [])  # llista plana de tots els monitors
    nits_lliures = assign_free_nights(monitors_this_week)
    meals_count_per_moni = {moni: 0 for moni in monitors_list}
    nits_desp_count_per_moni = {moni: 0 for moni in monitors_list}
    tl_count_per_moni = {moni: 0 for moni in monitors_list}
    # els anteriors diccionaris porten el recompte de les tasques que té assignades cada monitor.

    for day in week:
        week[day]["nit lliure"] = [m for m in nits_lliures[day]]
        for task in week[day]:
            if task == "nit lliure":
                continue
            monitors_ok = []
            monitors_not_ok = []
            limit = week[day][task][0]
            # utilitzaré la següent variable per comprovar que un grup sencer no estigui al mateix àpat
            monitors_copy = copy.deepcopy(monitors_this_week)

            while not len(monitors_ok) == limit:  # mentre no hi hagi el nombre suficient de monitors segueix buscant

                monitors_available = [x for x in monitors_list if x not in monitors_not_ok and x not in monitors_ok]

                if task in ["despertar", "nit"]:
                    nd_count_per_moni_availables = {moni: nits_desp_count_per_moni[moni] for moni in monitors_available}
                    if len(nd_count_per_moni_availables) == 0:
                        raise Exception("Error: there aren't monis availables for nd.")
                    minval = min(nd_count_per_moni_availables.values())
                    monis_with_less_nd = [k for k, v in nits_desp_count_per_moni.items()
                                          if v == minval and k in monitors_available]
                    monitor_try = random.choice(monis_with_less_nd)
                elif task in ["esmorzar", "dinar", "sopar"]:
                    meals_count_per_moni_availables = {moni: meals_count_per_moni[moni] for moni in monitors_available}
                    if len(meals_count_per_moni_availables) == 0:
                        raise Exception("Error: there aren't monis availables for meals.")
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

                if can_assign(group_monitor_try, monitor_try, day, task, nits_lliures):  # comprova si incompleix alguna restricció
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

    total_count_per_moni = {moni: nits_desp_count_per_moni[moni] + meals_count_per_moni[moni] +
                                  tl_count_per_moni[moni] for moni in monitors_list}

    total_count_no_travessa = {moni: nits_desp_count_per_moni[moni] + meals_count_per_moni[moni] +
                                     tl_count_per_moni[moni] for moni in monitors_list
                               if moni not in monitors_this_week["Travessa"]}

    meals_nd_counts_no_travessa = {moni: nits_desp_count_per_moni[moni] + meals_count_per_moni[moni]
                                   for moni in monitors_list if moni not in monitors_this_week["Travessa"]}

    meals_counts_no_travessa = {moni: meals_count_per_moni[moni] for moni in monitors_list
                                if moni not in monitors_this_week["Travessa"]}


    max_count_tasks = max(total_count_no_travessa.values())
    min_count_tasks = min(total_count_no_travessa.values())

    max_count_meals_nd = max(meals_nd_counts_no_travessa.values())
    min_count_meals_nd = min(meals_nd_counts_no_travessa.values())

    max_count_meals = max(meals_counts_no_travessa.values())
    min_count_meals = min(meals_counts_no_travessa.values())


    if max_count_tasks - min_count_tasks > 2:
        raise Exception("The distribution of tasks is too unbalanced")
    elif max_count_meals_nd - min_count_meals_nd > 1:
        raise Exception("The distribution of tasks is too unbalanced")
    elif max_count_meals - min_count_meals > 1:
        raise Exception("The distribution of tasks is too unbalanced")


    return week, nits_desp_count_per_moni, meals_count_per_moni, tl_count_per_moni, total_count_per_moni

