# Criptografía RSA

Universidad del Valle de Guatemala - MM2015 Matemática Discreta 1

## Integrantes

- Antony Portillo
- Jordi Cardona

## Instalación y ejecución

Se recomienda Python 3.12. El proyecto se verificó en Windows con Python 3.12.6 y Streamlit 1.45.0.

Abre una terminal en la carpeta que contiene `main.py`.

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

Si vuelves a abrir Terminal, ejecuta `source .venv/bin/activate` desde la carpeta del proyecto antes de iniciar la app.

La aplicación se abre en el navegador. Si necesitas abrirla manualmente, usa la dirección local que aparece en la terminal. Para detenerla, presiona `Ctrl+C` en la terminal.

## Llave pública en la aplicación

El enunciado solicita ingresar los primos `p`, `q` y el exponente `e` tanto al encriptar como al desencriptar. Por eso la aplicación no pide una llave pública ya construida: en cada operación calcula `n = p × q` y genera la llave pública `(e, n)`.

Durante la encriptación, la llave pública se muestra como resultado. Durante la desencriptación se vuelven a solicitar `p`, `q` y `e` porque son necesarios para calcular `φ(n)` y obtener el exponente privado `d`; una llave pública por sí sola no permite realizar ese cálculo.
