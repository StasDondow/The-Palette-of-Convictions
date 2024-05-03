import random
from math import sqrt


def chi(obs_is_act, obs_not_act):
    """ Функція обчислює статистику хі-квадрат. """

    # очікувана кількість активованих користувачів
    exp_is_act = sum(obs_is_act) / len(obs_is_act)
    # очікувана кількість неактивованих користувачів
    exp_not_act = sum(obs_not_act) / len(obs_not_act)

    # враховуємо поправку Єйтса
    R_is_act = [((abs(obs_is_act[i] - exp_is_act) - 0.5) / sqrt(exp_is_act)) ** 2 for i in range(len(obs_is_act))]
    R_not_act = [((abs(obs_not_act[i] - exp_not_act) - 0.5) / sqrt(exp_not_act)) ** 2 for i in range(len(obs_not_act))]
    return sum(R_is_act) + sum(R_not_act)


def bootstrap(groups, num_of_iterations):
    """ Функція обчислює p-value для критерію хі-квадрат методом повторного відбору. """

    # спостережувана кількість активованих користувачів
    obs_is_act = [x[0] for x in groups.values()]
    # спостережувана кількість неактивованих користувачів
    obs_not_act = [x[1] for x in groups.values()]

    # статистика хі-квадрат для наших даних
    obs_chi = chi(obs_is_act, obs_not_act)
    # кількість випадків, коли статистика хі-квадрат більша ніж в початкових даних
    bigger_chi = 0

    for i in range(num_of_iterations):
        # "складаємо в коробку" активованих та неактивованих користувачів
        box = [1] * sum(obs_is_act) + [0] * sum(obs_not_act)
        # перемішуємо
        random.shuffle(box)

        # поточна кількість активованих користувачів
        curr_obs_is_act = []
        # поточна кількість неактивованих користувачів
        curr_obs_not_act = []

        for j in range(len(groups)):
            # кількість активованих користувачів в поточній групі
            curr_group_cnt = sum(box[:obs_is_act[j] + obs_not_act[j]])
            # дадоємо активованих користувачів в поточній групі
            curr_obs_is_act.append(curr_group_cnt)
            # додаємо неактивованих користувачів в поточній групі
            curr_obs_not_act.append(obs_is_act[j] + obs_not_act[j] - curr_group_cnt)
            # відкидаємо викоритану частину групи
            box = box[obs_is_act[j] + obs_not_act[j]:]
        
        # поточна статистика хі-квадрат
        curr_chi = chi(curr_obs_is_act, curr_obs_not_act)
        if curr_chi > obs_chi: bigger_chi += 1

    # p-value
    return bigger_chi / num_of_iterations


if __name__ == "__main__":
    # для кожної групи записуємо кількість активованих та неактивованих користувачів
    groups = {
        0: [15, 64],
        1: [22, 48],
        2: [24, 56],
        3: [20, 49],
        4: [21, 49],
        5: [20, 40]
    }

    # кількість ітерацій бутстрапу
    num_of_iterations = 1000
    print(" p-value =", bootstrap(groups, num_of_iterations))
