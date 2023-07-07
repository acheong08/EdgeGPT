<div align="center">
  <img src="https://socialify.git.ci/acheong08/EdgeGPT/image?font=Inter&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F9%2F9c%2FBing_Fluent_Logo.svg&owner=1&pattern=Floating%20Cogs&theme=Auto" alt="EdgeGPT" width="640" height="320" />

# Edge GPT

_Ingeniería inversa al nuevo chat integrado en Bing_

<a href="./README.md">English</a> -
<a href="./README_zh-cn.md">简体中文</a> -
<a href="./README_zh-tw.md">繁體中文</a> -
<a>Español</a> -
<a href="./README_ja.md">日本語</a>

</div>

<p align="center">
  <a href="https://github.com/acheong08/EdgeGPT">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/EdgeGPT">
  </a>
  <img alt="Python version" src="https://img.shields.io/badge/python-3.8+-blue.svg">
  <img alt="Total downloads" src="https://static.pepy.tech/badge/edgegpt">

</p>

<details open>

<summary>

# Configuración

</summary>

## Instalación

```bash
python3 -m pip install EdgeGPT --upgrade
```

## Requisitos


- python 3.8+
- Una cuenta de Microsoft con acceso a <https://bing.com/chat> (Opcional, dependiendo de tu país)
- Estar localizado en un país con acceso al nuevo Bing (VPN necesaria para usarios de China)
- [Selenium](https://pypi.org/project/selenium/) (para la recolección automática de cookies)

## Autenticación

!!! ES PROBABLE QUE YA NO SEA NECESARIO !!!

**En algunas regiones**, Microsoft ha **abierto** la función de chat para todos,
por lo que es posible que **puedas saltarte este paso**.
Puedes comprobarlo con un navegador (con el user-agent modificado para parecer Edge),
**intentando abrir un chat sin haber iniciado sesión**.

Se ha encontrado que es posible que sea **dependiente de tu dirección IP**.
Por ejemplo, si intentas acceder a la función de chat desde una dirección IP que se conoce
que **pertenece al rango de un centro de datos** (vServers, servidores raíz, VPN, proxies conocidos, ...),
**es posible que tengas que iniciar sesión** y sin embargo puedas acceder sin problemas a las funciones
desde tu casa.

Si recibes el siguiente error, puedes probar **usando cookies** y viendo si funciona:

`Exception: Authentication failed. You have not been accepted into the beta.`

### Recolección de cookies

1. Necesitas un navegador que _parezca_ Microsoft Edge.

 * a) (Fácil) Instala la última versión de Microsoft Edge
 * b) (Avanzado) De forma alternativa, puedes usar cualquier navegador y
   cambiar el user-agent para que parezca que estás usando Edge
   (e.g., `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51`).
   Puedes hacer esto con extensiones del estilo "User-Agent Switcher and Manager" para [Chrome](https://chrome.google.com/webstore/detail/user-agent-switcher-and-m/bhchdcejhohfmigjafbampogmaanbfkg)
   o [Firefox](https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher/).

2. Abrir [bing.com/chat](https://bing.com/chat)
3. Si ves la nueva función de chat, es que puedes continuar...
4. Instala la extensión cookie editor para [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) o
   [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
5. Ve a [bing.com](https://bing.com)
6. Abre la extensión
7. Pulsa en "Export" abajo a la derecha, luego "Export as JSON" (Esto guarda la cookie en el portapapeles)
8. Pega el contenido en un fichero `bing_cookies_*.json`.
   * NOTA: Los **ficheros de cookies DEBEN seguir el siguiente formato de nombre `bing_cookies_*.json`**,
   de manera que puedan ser reconocidos por los mecanismos internos de procesado de cookies.



### Uso de la cookie en la librería:
```python
cookies = json.loads(open("./path/to/cookies.json", encoding="utf-8").read())  # might omit cookies option
bot = await Chatbot.create(cookies=cookies)
```

</details>

<details open>

<summary>

# Cómo usar Chatbot

</summary>

## Ejecución desde la línea de comandos

```
 $ python3 -m EdgeGPT.EdgeGPT -h

        EdgeGPT - A demo of reverse engineering the Bing GPT chatbot
        Repo: github.com/acheong08/EdgeGPT
        By: Antonio Cheong

        !help for help

        Type !exit to exit

usage: EdgeGPT.py [-h] [--enter-once] [--search-result] [--no-stream] [--rich] [--proxy PROXY] [--wss-link WSS_LINK]
                  [--style {creative,balanced,precise}] [--prompt PROMPT] [--cookie-file COOKIE_FILE]
                  [--history-file HISTORY_FILE] [--locale LOCALE]

options:
  -h, --help            show this help message and exit
  --enter-once
  --search-result
  --no-stream
  --rich
  --proxy PROXY         Proxy URL (e.g. socks5://127.0.0.1:1080)
  --wss-link WSS_LINK   WSS URL(e.g. wss://sydney.bing.com/sydney/ChatHub)
  --style {creative,balanced,precise}
  --prompt PROMPT       prompt to start with
  --cookie-file COOKIE_FILE
                        path to cookie file
  --history-file HISTORY_FILE
                        path to history file
  --locale LOCALE       your locale (e.g. en-US, zh-CN, en-IE, en-GB)
```
(China/US/UK/Norway disponen de mejor soporte para la localización)

## Ejecución en Python

### 1. La clase `Chatbot` y la librería `asyncio` para un control más exhaustivo

Usa Async para una mejor experiencia, por ejemplo:

```python
import asyncio, json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle

async def main():
    bot = await Chatbot.create() # Passing cookies is "optional", as explained above
    response = await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative, simplify_response=True)
    print(json.dumps(response, indent=2)) # Returns
    """
    {
        "text": str
        "author": str
        "sources": list[dict]
        "sources_text": str
        "suggestions": list[str]
        "messages_left": int
    }
    """
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### 2) Las clases auxiliares `Query` y `Cookie`

Realiza una petición a la IA de Bing Chat (usa el estilo 'precise' de conversación por defecto)
y devuelve la respuesta final sin ver todo el resultado de la API:

Recuerda almacenar las cookies en el formato: `bing_cookies_*.json`.

```python
from EdgeGPT.EdgeUtils import Query, Cookie

q = Query("What are you? Give your answer as Python code")
print(q)
```

También puedes cambiar el estilo de conversación o el fichero de cookie a usar:

```python
q = Query(
  "What are you? Give your answer as Python code",
  style="creative",  # or: 'balanced', 'precise'
  cookie_file="./bing_cookies_alternative.json"
)
```

Obtén rápidamente la respuesta, fragmentos de código, lista de fuentes/referencias,
o las preguntas sugeridas usando los siguientes atributos:

```python
q.output
q.code
q.suggestions
q.sources       # for the full json output
q.sources_dict  # for a dictionary of titles and urls
```

Obtén la pregunta inicial o el estilo de conversación usado:

```python
q.prompt
q.style
repr(q)
```

Accede a la lista de peticiones realizadas:

```python
Query.index  # A list of Query objects; updated dynamically
Query.request_count  # A tally of requests made using each cookie file
```

Finalmente, la clase `Cookie` admite múltiples ficheros de cookie, de manera que
si has creado ficheros adicionales de cookies usando el formato de nombrado
`bing_cookies_*.json`, las peticiones intentarán usar automáticamente el siguiente
fichero (alfabéticamente) si has sobrepasado el límite diario de peticiones (actualmente limitado a 200).

Principales atributos que tienes a disposición:

```python
Cookie.current_file_index
Cookie.dirpath
Cookie.search_pattern  # default is `bing_cookies_*.json`
Cookie.files()  # list as files that match .search_pattern
Cookie.current_filepath
Cookie.current_data
Cookie.import_next()
Cookie.image_token
Cookie.ignore_files
```

---

## Ejecución en Docker

Este ejemplo asume que dispones de un fichero `cookies.json` en tu directorio actual

```bash

docker run --rm -it -v $(pwd)/cookies.json:/cookies.json:ro -e COOKIE_FILE='/cookies.json' ghcr.io/acheong08/edgegpt
```

Puedes añadir argumentos adicionales de la siguiente manera

```bash

docker run --rm -it -v $(pwd)/cookies.json:/cookies.json:ro -e COOKIE_FILE='/cookies.json' ghcr.io/acheong08/edgegpt --rich --style creative
```

</details>

</details>

<details open>

<summary>

# Cómo usar Image generator

</summary>

## Ejecución desde la línea de comandos

```bash
$ python3 -m ImageGen.ImageGen -h
usage: ImageGen.py [-h] [-U U] [--cookie-file COOKIE_FILE] --prompt PROMPT [--output-dir OUTPUT_DIR] [--quiet] [--asyncio]

optional arguments:
  -h, --help            show this help message and exit
  -U U                  Auth cookie from browser
  --cookie-file COOKIE_FILE
                        File containing auth cookie
  --prompt PROMPT       Prompt to generate images for
  --output-dir OUTPUT_DIR
                        Output directory
  --quiet               Disable pipeline messages
  --asyncio             Run ImageGen using asyncio
```

## Ejecución en Python

### 1) La clase auxiliar `ImageQuery`

Genera imágenes de acuerdo a la petición y las descarga en el directorio actual

```python
from EdgeGPT.EdgeUtils import ImageQuery

q=ImageQuery("Meerkats at a garden party in Devon")
```

Cambia el directorio de descarga para las demás imágenes que se descarguen durante el resto de sesión

```
Query.image_dirpath = Path("./to_another_folder")
```

### 2) Usa las clases `ImageGen` y `asyncio` para un control más minucioso

```python
from EdgeGPT.ImageGen import ImageGen
import argparse
import json

async def async_image_gen(args) -> None:
    async with ImageGenAsync(args.U, args.quiet) as image_generator:
        images = await image_generator.get_images(args.prompt)
        await image_generator.save_images(images, output_dir=args.output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-U", help="Auth cookie from browser", type=str)
    parser.add_argument("--cookie-file", help="File containing auth cookie", type=str)
    parser.add_argument(
        "--prompt",
        help="Prompt to generate images for",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory",
        type=str,
        default="./output",
    )
    parser.add_argument(
        "--quiet", help="Disable pipeline messages", action="store_true"
    )
    parser.add_argument(
        "--asyncio", help="Run ImageGen using asyncio", action="store_true"
    )
    args = parser.parse_args()
    # Load auth cookie
    with open(args.cookie_file, encoding="utf-8") as file:
        cookie_json = json.load(file)
        for cookie in cookie_json:
            if cookie.get("name") == "_U":
                args.U = cookie.get("value")
                break

    if args.U is None:
        raise Exception("Could not find auth cookie")

    if not args.asyncio:
        # Create image generator
        image_generator = ImageGen(args.U, args.quiet)
        image_generator.save_images(
            image_generator.get_images(args.prompt),
            output_dir=args.output_dir,
        )
    else:
        asyncio.run(async_image_gen(args))

```

</details>

<details open>

<summary>

# Historial de estrellas

</summary>

[![Gráfica historial de estrellas](https://api.star-history.com/svg?repos=acheong08/EdgeGPT&type=Date)](https://star-history.com/#acheong08/EdgeGPT&Date)

</details>

<details open>

<summary>

# Contribuidores

</summary>

Este proyecto existe gracias a todas las personas que apoyan y contribuyen.

 <a href="https://github.com/acheong08/EdgeGPT/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=acheong08/EdgeGPT" />
 </a>

</details>
