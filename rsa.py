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


def encriptar(mensaje, p, q, e):
    n, phi = calcular_parametros(p, q, e)

    if not mensaje:
        raise ValueError("Ingresa al menos un carácter.")

    for caracter in mensaje:
        if not 32 <= ord(caracter) <= 126:
            raise ValueError("El mensaje solo puede contener caracteres ASCII imprimibles (Estas ingresando caracters que no se permiten en este proyecto)")

    longitud = len(mensaje)
    relleno = longitud % 2 == 1
    texto = mensaje
    if relleno:
        texto += " "

    bloques_cifrados = []
    detalle = []
    for posicion in range(0, len(texto), 2):
        pareja = texto[posicion:posicion + 2]
        ascii_1 = f"{ord(pareja[0]):03d}"
        ascii_2 = f"{ord(pareja[1]):03d}"
        bloque_original = ascii_1 + ascii_2
        bloque_cifrado = f"{potencia_modular(int(bloque_original), e, n):06d}"

        bloques_cifrados.append(bloque_cifrado)
        detalle.append({
            "caracteres": pareja,
            "ascii_1": ascii_1,
            "ascii_2": ascii_2,
            "bloque_original": bloque_original,
            "bloque_cifrado": bloque_cifrado,
        })

    return {
        "cifrado": " ".join(bloques_cifrados),
        "longitud": longitud,
        "relleno": relleno,
        "n": n,
        "phi": phi,
        "llave_publica": (e, n),
        "bloques": detalle,
    }


def leer_bloques_cifrados(cifrado, n):
    if not cifrado:
        raise ValueError("Ingresa al menos un bloque de seis dígitos.")

    bloques = cifrado.split(" ")
    for bloque in bloques:
        if len(bloque) != 6 or not bloque.isascii() or not bloque.isdecimal():
            raise ValueError("Escribe bloques de seis dígitos separados por un solo espacio.")
        if int(bloque) >= n:
            raise ValueError(f"El bloque {bloque} debe ser menor que n ({n}).")

    return bloques


def desencriptar(cifrado, longitud, p, q, e):
    n, phi = calcular_parametros(p, q, e)
    bloques_cifrados = leer_bloques_cifrados(cifrado, n)
    longitud_con_relleno = len(bloques_cifrados) * 2

    if type(longitud) is not int or longitud not in (longitud_con_relleno, longitud_con_relleno - 1):
        raise ValueError(
            f"Para {len(bloques_cifrados)} bloque(s), L debe ser "
            f"{longitud_con_relleno - 1} o {longitud_con_relleno}."
        )

    d = inverso_modular(e, phi)
    parejas = []
    detalle = []
    for bloque_cifrado in bloques_cifrados:
        bloque_original = f"{potencia_modular(int(bloque_cifrado), d, n):06d}"
        ascii_1 = bloque_original[:3]
        ascii_2 = bloque_original[3:]
        codigo_1 = int(ascii_1)
        codigo_2 = int(ascii_2)
        if not (32 <= codigo_1 <= 126 and 32 <= codigo_2 <= 126):
            raise ValueError(f"El bloque {bloque_cifrado} no produce dos caracteres ASCII válidos")

        pareja = chr(codigo_1) + chr(codigo_2)
        parejas.append(pareja)
        detalle.append({
            "caracteres": pareja,
            "ascii_1": ascii_1,
            "ascii_2": ascii_2,
            "bloque_original": bloque_original,
            "bloque_cifrado": bloque_cifrado,
        })

    mensaje = "".join(parejas)
    relleno = longitud % 2 == 1
    if relleno:
        if not mensaje.endswith(" "):
            raise ValueError("Falta el espacio de relleno al final del mensaje")
        mensaje = mensaje[:-1]

    return {
        "mensaje": mensaje,
        "longitud": longitud,
        "relleno": relleno,
        "n": n,
        "phi": phi,
        "d": d,
        "bloques": detalle,
    }
