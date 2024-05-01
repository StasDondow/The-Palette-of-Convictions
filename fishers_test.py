from math import factorial as f


def exact_probability(a, b, c, d):
  """ Формула точної ймовірності спостерігати такий розподіл даних, як у вибірці. """
   
  # суми значень в рядках таблиці 
  r1 = a + b; r2 = c + d 
  # суми значень в колонках таблиці
  c1 = a + c; c2 = b + d 
  # загальна сума елементів таблиці
  n = c1 + c2

  return f(r1) * f(r2) * f(c1) * f(c2) /  \
          (f(n) * f(a) * f(b) * f(c) * f(d))


def fisher(a, b, c, d):
  """ Функція повертає суму ймовірностей спостерігати такий розподіл як в даних, або більш екстремальний. 
  Двосторонній тест Фішера. """
  
  # ймовірність спостерігати такий розподіл як в даних 
  p0 = exact_probability(a, b, c, d)

  # p-value
  p = 0
  p += p0

  # значення елементів поточної таблиці
  curr_a = a; curr_b = b; curr_c = c; curr_d = d

  while True:
    # збільшуємо значення на головній діагоналі
    curr_a += 1; curr_d += 1
    # зменшуємо значення на побічній діагоналі
    curr_b -= 1; curr_c -=1

    if curr_a >= 0 and curr_b >= 0 and curr_c >= 0 and curr_d >= 0:
      curr_p = exact_probability(curr_a, curr_b, curr_c, curr_d)
      if curr_p <= p0: p += curr_p
    else:
      break

  curr_a = a; curr_b = b; curr_c = c; curr_d = d

  while True:
    # збільшуємо значення на побічній діагоналі
    curr_b += 1; curr_c +=1
    # зменшуємо значення на головній діагоналі
    curr_a -= 1; curr_d -= 1

    if curr_a >= 0 and curr_b >= 0 and curr_c >= 0 and curr_d >= 0:
      curr_p = exact_probability(curr_a, curr_b, curr_c, curr_d)
      if curr_p <= p0: p += curr_p
    else:
      break

  return p


if __name__ == "__main__":
  a = int(input(" a = "))
  b = int(input(" b = "))
  c = int(input(" c = "))
  d = int(input(" d = "))
  print("\n p-value =", round(fisher(a, b, c, d), 3))
