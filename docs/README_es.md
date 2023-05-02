<div align="center">
  <img src="https://socialify.git.ci/acheong08/EdgeGPT/image?font=Inter&language=1&logo=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2F9%2F9c%2FBing_Fluent_Logo.svg&owner=1&pattern=Floating%20Cogs&theme=Auto" alt="EdgeGPT" width="640" height="320" />

# Edge GPT

_Ingeniería inversa al nuevo chat integrado en Bing_

<a href="./README.md">English</a> -
<a href="./README_zh-cn.md">简体中文</a> -
<a href="./README_zh-tw.md">繁體中文 (中國臺灣)</a> -
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

---

## Configuración

### Instalación de dependencias

```bash
python3 -m pip install EdgeGPT --upgrade
```

### Requisitos

- python 3.8+
- Una cuenta de Microsoft con acceso a <https://bing.com/chat> (Obligatorio)
- Estar localizado en una región con soporte para el nuevo Bing (para usuarios en China es necesario el uso de VPN)

<details>
  <summary>

### Comprobar el acceso (Obligatorio)

  </summary>

- Instalar la última versión de Microsoft Edge
- Es posible configurar el user-agent para imitar el navegador Edge (p. ej., `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.51`). Puedes realizar esto fácilmente mediante extensiones como "User-Agent Switcher and Manager" para [Chrome](https://chrome.google.com/webstore/detail/user-agent-switcher-and-m/bhchdcejhohfmigjafbampogmaanbfkg) y [Firefox](https://addons.mozilla.org/en-US/firefox/addon/user-agent-string-switcher/).
- Abrir [bing.com/chat](https://bing.com/chat)
- Si ves disponible el nuevo chat, todo estaría correcto y podrías continuar

</details>

<details>
  <summary>

### Obteniendo las cookies de autenticación (Obligatorio)

  </summary>

- Instala la extensión para editar cookies en [Chrome](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) o [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/)
- Ve a `bing.com`
- Abre la extensión
- Presiona en "Export" en la parte inferior derecha y luego en "Export as JSON" (Esto guarda las cookies en el portapapeles)
- Pega las cookies en el fichero `cookies.json`

</details>

<details>

<summary>

## Chatbot

</summary>

## Uso

### Ejemplo línea de comandos

```
 $ python3 -m EdgeGPT -h

        EdgeGPT - A demo of reverse engineering the Bing GPT chatbot
        Repo: github.com/acheong08/EdgeGPT
        By: Antonio Cheong

        !help for help

        Type !exit to exit
        Enter twice to send message or set --enter-once to send one line message

usage: EdgeGPT.py [-h] [--enter-once] [--no-stream] [--rich] [--proxy PROXY] [--wss-link WSS_LINK] [--style {creative,balanced,precise}]
                  [--cookie-file COOKIE_FILE]

options:
  -h, --help            show this help message and exit
  --enter-once
  --no-stream
  --rich
  --proxy PROXY         Proxy URL (e.g. socks5://127.0.0.1:1080)
  --wss-link WSS_LINK   WSS URL(e.g. wss://sydney.bing.com/sydney/ChatHub)
  --style {creative,balanced,precise}
  --cookie-file COOKIE_FILE
                        needed if environment variable COOKIE_FILE is not set
```

---

### Ejemplo para desarrolladores

Es posible pasar las cookies a EdgeGPT de tres maneras:

- Usando una variable de entorno: `export COOKIE_FILE=/path/to/cookies.json`.
- Especificando la ruta a `cookies.json` en el argumento `cookie_path`:

  ```python
  bot = Chatbot(cookie_path='./cookie.json')
  ```

- Pasando las cookies directamente mediante el argumento `cookies`:

  ```python
  with open('./cookie.json', 'r') as f:
      cookies = json.load(f)
  bot = Chatbot(cookies=cookies)
  ```

Usa programación asíncrona para una mejor experiencia de usuario

Código de ejemplo usando programación asíncrona:

```python
import asyncio
from EdgeGPT import Chatbot, ConversationStyle

async def main():
    bot = await Chatbot.create()
    print(await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative, wss_link="wss://sydney.bing.com/sydney/ChatHub"))
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

```

</details>

<details>

<summary>

## Generación de imágenes

</summary>

```bash
$ python3 -m ImageGen -h
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

### Ejemplo para desarrolladores

```python
from ImageGen import ImageGen
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

## Historial de estrellas

[![Star History Chart](https://api.star-history.com/svg?repos=acheong08/EdgeGPT&type=Date)](https://star-history.com/#acheong08/EdgeGPT&Date)

## Contribuidores

Este proyecto existe gracias a todas las personas que apoyan y contribuyen.

 <a href="https://github.com/acheong08/EdgeGPT/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=acheong08/EdgeGPT" />
 </a>
