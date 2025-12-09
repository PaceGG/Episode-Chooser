def maximize_a(a: str, b: str) -> str:
    b_conut = [0] * 10
    for ch in b:
        b_conut[ord(ch) - 48] += 1  # '0' -> 48

    print(b_conut)

    a_list = list(a)
    for i, ch in enumerate(a_list):
        cur = ord(ch) - 48
        d = 9
        while d > cur and b_conut[d] == 0:
            d -= 1
        if d > cur:
            a_list[i] = chr(d + 48)
            b_conut[d] -= 1

    return "".join(a_list)


# Примеры
print(maximize_a("00003", "4"))     # -> "873"
print(maximize_a("932", "01"))     # -> "932"
print(maximize_a("1234", "4321"))  # -> "4234"



print(maximize_a("523", "87"))     # -> "873" (заменили 5 на 8, 2 на 7)
print(maximize_a("932", "01"))     # -> "932" (никакая замена не улучшает)
print(maximize_a("1234", "4321"))  # -> "4234" (берём 4 для первого разряда, затем 3 не заменит 2? смотрите шаги)
