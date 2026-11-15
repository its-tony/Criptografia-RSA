# Criptografía RSA
Universidad del Valle de Guatemala 2026 

**Integrantes** — Antony Portillo y Jordi Cardona

La aplicación encripta y desencripta mensajes de texto con RSA y muestra la conversión ASCII y los cálculos por bloque.

## VIDEO

https://youtu.be/948Idriwf1o (lo recomendamos ver primero antes de probar el programa)

## Instalación y ejecución

Se recomienda Python 3.12. El proyecto se verificó en Windows con Python 3.12.6 y Streamlit 1.45.0.

Se tiene que abrir una terminal en la carpeta que contiene `main.py` (la principal).

### Windows (PowerShell)

```powershell
python -m pip install -r requirements.txt
python -m streamlit run main.py
```

### macOS (Terminal)

Con Python 3.12 instalado, crea y activa un entorno virtual antes de instalar las dependencias.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run main.py
```

Si vuelve a abrir Terminal, ejecute `source .venv/bin/activate` desde la carpeta del proyecto antes de iniciar la app.

La aplicación se abre en el navegador. Si necesitas abrirla manualmente, use la dirección local que aparece en la terminal. Para detener el programa, presione `Ctrl+C` en la terminal. o en mac `cmd+C`

## Uso y ejemplo completo

### Encriptar

1. En la pestaña **Encriptar**, escribe `RSA` en **Mensaje original (M)**. Usa `p = 367`, `q = 373` y `e = 17`.
2. Presiona **Encriptar**. Debajo del formulario, **Cifrado (C)** muestra `026054 123875` y **Longitud original (L)** muestra `3`. Guarda ambos valores para desencriptar.
3. El resumen muestra `n = 136891`, `φ = 136152`, la llave pública `(17, 136891)` y que se agregó un espacio de relleno. En **Detalle por bloque** puedes comprobar estas conversiones:

   | Caracteres | Códigos ASCII | Bloque original | Bloque cifrado |
   | --- | --- | --- | --- |
   | `RS` | `082` y `083` | `082083` | `026054` |
   | `A␠` | `065` y `032` | `065032` | `123875` |

   El símbolo `␠` es un espacio en la tabla.

### Desencriptar

1. En la pestaña **Desencriptar**, pega `026054 123875` en **Cifrado (C)** e ingresa `3` en **Longitud original (L)**. Usa los mismos valores de `p`, `q` y `e`.
2. Presiona **Desencriptar**. **Mensaje recuperado (M)** muestra `RSA` y el resumen muestra el exponente privado `d = 8009`.
3. Separa los bloques con un solo espacio y conserva los seis dígitos de cada bloque, incluidos los ceros iniciales. Pega el cifrado sin espacios al inicio ni al final.

Para ver un error de validación, cambia `L` a `2` con el mismo cifrado. Hay dos bloques, así que las longitudes posibles son `3` y `4`.

## Cómo funciona el relleno

Cada bloque contiene dos caracteres ASCII imprimibles, con códigos del 32 al 126. Si la longitud original `L` es impar, se agrega un espacio al final para completar la última pareja. Si `L` es par, se conservan los caracteres tal como se ingresaron.

Al desencriptar con `L` impar, el programa comprueba que el último carácter sea un espacio y retira exactamente ese carácter. Se conservan todos los espacios originales, incluso si el mensaje está formado solo por espacios. La entrada se rechaza si está vacía o contiene caracteres fuera del rango permitido.

## Archivos y algoritmos

- [`main.py`](main.py) contiene la interfaz de Streamlit y es el punto de entrada.
- [`rsa.py`](rsa.py) contiene las validaciones y la lógica de RSA. Las funciones propias son `mcd` (algoritmo de Euclides), `bezout_matricial` e `inverso_modular` (para obtener `d`), y `potencia_modular` (cuadrados sucesivos). La función `es_primo` verifica la primalidad por división de prueba.
- [`requirements.txt`](requirements.txt) indica la versión de Streamlit usada.


## Archivos y algoritmos
Cualquier consulta estamos a la dispoción de resolverla :)