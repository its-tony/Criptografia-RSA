def es_primo(numero: int) -> bool:
    if numero < 2:
        return False

    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 1

    return True


def mcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b

    return a


def bezout_matricial(a: int, b: int) -> tuple[int, int]:
    """Devuelve (x, y) con a*x + b*y = MCD(a, b)."""

    if type(a) is not int or type(b) is not int:
        raise TypeError("a y b deben ser enteros.")
    if a < 1 or b < 1:
        raise ValueError("a y b deben ser positivos.")

    cocientes = []
    while b != 0:
        cociente = a // b
        residuo = a % b
        cocientes.append(cociente)
        a = b
        b = residuo

    cocientes.pop()

    matriz = [[1, 0], [0, 1]]
    for cociente in cocientes:
        matriz = [
            [matriz[0][0] * cociente + matriz[0][1], matriz[0][0]],
            [matriz[1][0] * cociente + matriz[1][1], matriz[1][0]],
        ]

    signo = 1 if len(cocientes) % 2 == 0 else -1
    inversa = [
        [matriz[1][1] * signo, -matriz[0][1] * signo],
        [-matriz[1][0] * signo, matriz[0][0] * signo],
    ]

    return inversa[1][0], inversa[1][1]


def inverso_modular(numero: int, modulo: int) -> int:
    x, _ = bezout_matricial(numero, modulo)
    return x % modulo


def potencia_modular(base: int, exponente: int, modulo: int) -> int:
    """Calcula base**exponente (mod modulo) por cuadrados sucesivos."""

    resultado = 1
    base = base % modulo

    while exponente > 0:
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo
        base = (base * base) % modulo
        exponente //= 2

    return resultado


def calcular_parametros(p: int, q: int, e: int) -> tuple[int, int]:
    if p == q:
        raise ValueError("p y q deben ser primos distintos.")
    if not es_primo(p) or not es_primo(q):
        raise ValueError("p y q deben ser números primos.")

    n = p * q
    if not 126126 < n < 1000000:
        raise ValueError("p × q debe estar entre 126126 y 1000000, sin incluirlos.")

    phi = (p - 1) * (q - 1)
    if e <= 1:
        raise ValueError("e debe ser mayor que 1.")
    if mcd(e, phi) != 1:
        raise ValueError("El MCD de e y φ debe ser 1.")

    return n, phi


def encriptar(mensaje: str, p: int, q: int, e: int) -> dict:
    n, phi = calcular_parametros(p, q, e)

    if not mensaje:
        raise ValueError("Ingresa al menos un carácter.")

    for caracter in mensaje:
        if not 32 <= ord(caracter) <= 126:
            raise ValueError("El mensaje solo puede contener caracteres ASCII imprimibles.")

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


def leer_bloques_cifrados(cifrado: str, n: int) -> list[str]:
    if not cifrado:
        raise ValueError("Ingresa al menos un bloque de seis dígitos.")

    bloques = cifrado.split(" ")
    for bloque in bloques:
        if len(bloque) != 6 or not bloque.isascii() or not bloque.isdecimal():
            raise ValueError("Escribe bloques de seis dígitos separados por un solo espacio.")
        if int(bloque) >= n:
            raise ValueError(f"El bloque {bloque} debe ser menor que n ({n}).")

    return bloques


def desencriptar(cifrado: str, longitud: int, p: int, q: int, e: int) -> dict:
    n, phi = calcular_parametros(p, q, e)
    bloques_cifrados = leer_bloques_cifrados(cifrado, n)
    longitud_con_relleno = len(bloques_cifrados) * 2

    if longitud not in (longitud_con_relleno, longitud_con_relleno - 1):
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
