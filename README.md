# Criptografía RSA

Universidad del Valle de Guatemala - MM2015 Matemática Discreta 1

**Integrantes:** Antony Portillo y Jordi Cardona.

Esta aplicación permite encriptar y desencriptar mensajes de texto con RSA. Durante el proceso se puede ver la conversión ASCII de cada bloque y los cálculos más importantes.

## Instalación y ejecución

Recomendamos usar Python 3.12. El proyecto se probó en Windows con Python 3.12.6 y Streamlit 1.45.0. Para iniciar, abre una terminal dentro de la carpeta que contiene `main.py`.

### Windows (PowerShell)

```powershell
python -m pip install -r requirements.txt
python -m streamlit run main.py
```

### macOS (Terminal)

Con Python 3.12 instalado, crea y activa un entorno virtual antes de instalar las dependencias:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run main.py
```

Si más adelante vuelves a abrir Terminal, primero ejecuta `source .venv/bin/activate` desde la carpeta del proyecto. La aplicación se abrirá en el navegador; si no ocurre, copia la dirección local que aparece en la terminal. Para detenerla, presiona `Ctrl+C`.

## Uso

### Encriptar

En la pestaña **Encriptar**, escribe el mensaje original `M` e ingresa los primos `p`, `q` y el exponente `e`. Al presionar **Encriptar**, verás el cifrado completo `C`, la longitud original `L`, la llave pública `(e, n)`, los valores de `n` y `φ(n)`, el relleno aplicado y el detalle ASCII de los bloques.

Guarda `C` y `L`: son los datos que se necesitan para recuperar el mensaje.

### Desencriptar

En la pestaña **Desencriptar**, pega `C` exactamente como aparece —bloques de seis dígitos separados por un espacio—, ingresa `L` y usa los mismos valores de `p`, `q` y `e`. Al presionar **Desencriptar**, la aplicación calcula `d` y muestra el mensaje recuperado `M` junto con el detalle de bloques.

No hay un campo para escribir una llave pública ya construida porque el enunciado pide `p`, `q` y `e` en las dos operaciones. Con esos valores, la aplicación calcula `n = p × q` y forma la llave pública `(e, n)` cada vez. Además, para descifrar se necesitan `p` y `q`: permiten calcular `φ(n)` y obtener el exponente privado `d`.

## Ejemplo

Por ejemplo, para encriptar `RSA`, usa `p = 367`, `q = 373` y `e = 17`. La aplicación produce:

- `C = 026054 123875`
- `L = 3`
- llave pública `(17, 136891)`

Para desencriptar, ingresa ese mismo `C`, `L = 3` y los mismos valores de `p`, `q` y `e`. El resultado será el mensaje `RSA` y el exponente privado `d = 8009`.

## Relleno

Cada bloque guarda dos caracteres ASCII imprimibles. Si el mensaje tiene una longitud `L` impar, se añade un espacio al final para completar la última pareja. Al desencriptar, ese espacio se quita solo cuando `L` es impar; los espacios que el mensaje tenía originalmente, incluso los del inicio o del final, se conservan.

## Archivos, algoritmos y validaciones

- [`main.py`](main.py) contiene la interfaz de Streamlit.
- [`rsa.py`](rsa.py) reúne la lógica RSA: `mcd` calcula el máximo común divisor; `bezout_matricial` e `inverso_modular` obtienen `d`; y `potencia_modular` hace la exponenciación modular por cuadrados sucesivos. `es_primo` revisa que `p` y `q` sean primos.
- [`requirements.txt`](requirements.txt) indica la versión de Streamlit que necesita el proyecto.

El programa revisa que `p` y `q` sean primos distintos, que `n` esté dentro del rango pedido y que `e` sea mayor que uno y coprimo con `φ(n)`. También avisa si el mensaje contiene caracteres no permitidos, si el cifrado tiene bloques mal formados o fuera de rango, si `L` no coincide con la cantidad de bloques o si el resultado no recupera caracteres ASCII válidos y el relleno esperado.
