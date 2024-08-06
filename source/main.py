import tools

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

    monitors_dict = {}

    # week_num = int(input("Introdueix el número de la setmana: "))
    #
    # for group_name in groups[week_num]:
    #     names = input(f"Introdueix els noms dels monitors de {group_name}: separats per comes: ").split(",")
    #     monitors_dict[group_name] = [name.strip() for name in names]

    monitors_dict = {"Av Cabirols": ["Eva", "Pau"], "Av Isards": ["Blanca", "Erola"],
                          "Bold Adv": ["Laia", "Júlia", "Noa"], "Wild Adv": ["Vinyet", "Max", "Lara"],
                          "Equitació avançat": ["Manel", "Irene"]}
    return monitors_dict

def run():
    success = False
    attempts = 0
    max_attempts = 500

    monitors_this_week = get_groups()
    while not success and attempts < max_attempts:
        attempts += 1
        try:
            prova, nits_counts, meals_counts, tl_counts, total_counts = tools.assign_names_to_tasks(monitors_this_week)
            success = True
            for d in prova.items():
                print(d)

            print("\n NITS\n", nits_counts)
            print("\n MEALS\n", meals_counts)
            print("\n TL\n", tl_counts)
            print("\n TOTALS\n", total_counts)

        except Exception as e:
            print(f"Attempt {attempts} failed: {e}. Trying again...")

    if not success:
        print("Failed to complete the algorithm after maximum attempts.")

if __name__ == "__main__":
    run()