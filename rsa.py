def es_primo(numero):
    if numero < 2:
        return False

    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 1

    return True


def mcd(a, b):
    a = abs(a)
    b = abs(b)

    while b != 0:
        a, b = b, a % b

    return a


def inverso_modular(numero, modulo):
    resto_anterior, resto = modulo, numero % modulo
    coeficiente_anterior, coeficiente = 0, 1
# estos coeficientes indican cuánto aporta el número a cada resto
    while resto != 0:
        cociente = resto_anterior // resto
        resto_anterior, resto = resto, resto_anterior % resto
        coeficiente_anterior, coeficiente = (
            coeficiente,
            coeficiente_anterior - cociente * coeficiente,
        )

    if resto_anterior != 1:
        raise ValueError("El número no tiene inverso para este módulo.")

    return coeficiente_anterior % modulo


def potencia_modular(base, exponente, modulo):
    resultado = 1 % modulo
    base = base % modulo

# cada vuelta usa un dígito del exponente en binario
    while exponente > 0:
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        exponente //= 2

    return resultado


def calcular_parametros(p, q, e):
    
#todo eso es programación defensiva, para que el usuario no meta la pata :)
    if type(p) is not int or type(q) is not int or type(e) is not int:
        raise ValueError("p, q y e deben ser números enteros")

    if p < 2 or q < 2:
        raise ValueError("p y q deben ser números primos ")
    if p == q:
        raise ValueError("p y q deben ser distintos ")

    n = p * q
    if not 126126 < n < 1000000:
        raise ValueError("El producto p × q debe estar entre 126126 y 1000000, sin incluirlos")
    if not es_primo(p) or not es_primo(q):
        raise ValueError("p y q deben ser números primos ")

    phi = (p - 1) * (q - 1)
    if e <= 1:
        raise ValueError("e debe ser mayor que 1.")
    if mcd(e, phi) != 1:
        raise ValueError("El MCD de e y phi debe ser 1.")

    return n, phi
