import asyncio
import contextlib
import json
import os
import sys
import time

import aiohttp
import regex
import requests
import argparse
import pkg_resources

BING_URL = "https://www.bing.com"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "referrer": "https://www.bing.com/images/create/",
    "origin": "https://www.bing.com",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63",
}


class ImageGen:
    """
    Image generation by Microsoft Bing
    Parameters:3
        auth_cookie: str
    """

    def __init__(self, auth_cookie: str, quiet: bool = False) -> None:
        self.session: requests.Session = requests.Session()
        self.session.headers = HEADERS
        self.session.cookies.set("_U", auth_cookie)
        self.quiet = quiet

    def get_images(self, prompt: str) -> list:
        """
        Fetches image links from Bing
        Parameters:
            prompt: str
        """
        if not self.quiet:
            print("Sending request...")
        url_encoded_prompt = requests.utils.quote(prompt)
        # https://www.bing.com/images/create?q=<PROMPT>&rt=3&FORM=GENCRE
        url = f"{BING_URL}/images/create?q={url_encoded_prompt}&rt=4&FORM=GENCRE"
        response = self.session.post(url, allow_redirects=False)
        # check for content waring message
        if "this prompt has been blocked" in response.text.lower():
            raise Exception(
                "Your prompt has been blocked by Bing. Try to change any bad words and try again."
            )
        if response.status_code != 302:
            # if rt4 fails, try rt3
            url = f"{BING_URL}/images/create?q={url_encoded_prompt}&rt=3&FORM=GENCRE"
            response3 = self.session.post(url, allow_redirects=False, timeout=200)
            if response3.status_code != 302:
                print(f"ERROR: {response3.text}")
                raise Exception(
                    "Redirect failed, also possible that this prompt isn't allowed"
                )
            response = response3
        # Get redirect URL
        redirect_url = response.headers["Location"].replace("&nfy=1", "")
        request_id = redirect_url.split("id=")[-1]
        self.session.get(f"{BING_URL}{redirect_url}")
        # https://www.bing.com/images/create/async/results/{ID}?q={PROMPT}
        polling_url = f"{BING_URL}/images/create/async/results/{request_id}?q={url_encoded_prompt}"
        # Poll for results
        if not self.quiet:
            print("Waiting for results...")
        start_wait = time.time()
        while True:
            if int(time.time() - start_wait) > 200:
                raise Exception("Timeout error")
            if not self.quiet:
                print(".", end="", flush=True)
            response = self.session.get(polling_url)
            if response.status_code != 200:
                raise Exception("Could not get results")
            if not response.text:
                time.sleep(1)
                continue
            else:
                break
        # Use regex to search for src=""
        image_links = regex.findall(r'src="([^"]+)"', response.text)
        # Remove size limit
        normal_image_links = [link.split("?w=")[0] for link in image_links]
        # Remove duplicates
        normal_image_links = list(set(normal_image_links))

        # Bad images
        bad_images = [
            "https://r.bing.com/rp/in-2zU3AJUdkgFe7ZKv19yPBHVs.png",
            "https://r.bing.com/rp/TX9QuO3WzcCJz1uaaSwQAz39Kb0.jpg",
        ]
        for img in normal_image_links:
            if img in bad_images:
                raise Exception("Bad images")
        # No images
        if not normal_image_links:
            raise Exception("No images")
        return normal_image_links

    def save_images(self, links: list, output_dir: str) -> None:
        """
        Saves images to output directory
        """
        if not self.quiet:
            print("\nDownloading images...")
        with contextlib.suppress(FileExistsError):
            os.mkdir(output_dir)
        try:
            for image_num, link in enumerate(links):
                with self.session.get(link, stream=True) as response:
                    # save response to file
                    response.raise_for_status()
                    with open(f"{output_dir}/{image_num}.jpeg", "wb") as output_file:
                        for chunk in response.iter_content(chunk_size=8192):
                            output_file.write(chunk)
        except requests.exceptions.MissingSchema as url_exception:
            raise Exception(
                "Inappropriate contents found in the generated images. Please try again or try another prompt."
            ) from url_exception


class ImageGenAsync:
    """
    Image generation by Microsoft Bing
    Parameters:
        auth_cookie: str
    """

    def __init__(self, auth_cookie: str, quiet: bool = False) -> None:
        self.session = aiohttp.ClientSession(
            headers=HEADERS,
            cookies={"_U": auth_cookie},
        )
        self.quiet = quiet

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo) -> None:
        await self.session.close()

    async def get_images(self, prompt: str) -> list:
        """
        Fetches image links from Bing
        Parameters:
            prompt: str
        """
        if not self.quiet:
            print("Sending request...")
        url_encoded_prompt = requests.utils.quote(prompt)
        # https://www.bing.com/images/create?q=<PROMPT>&rt=3&FORM=GENCRE
        url = f"{BING_URL}/images/create?q={url_encoded_prompt}&rt=4&FORM=GENCRE"
        async with self.session.post(url, allow_redirects=False) as response:
            content = await response.text()
            if "this prompt has been blocked" in content.lower():
                raise Exception(
                    "Your prompt has been blocked by Bing. Try to change any bad words and try again."
                )
            if response.status != 302:
                # if rt4 fails, try rt3
                url = (
                    f"{BING_URL}/images/create?q={url_encoded_prompt}&rt=3&FORM=GENCRE"
                )
                async with self.session.post(
                    url,
                    allow_redirects=False,
                    timeout=200,
                ) as response3:
                    if response3.status != 302:
                        print(f"ERROR: {response3.text}")
                        raise Exception("Redirect failed")
                    response = response3
        # Get redirect URL
        redirect_url = response.headers["Location"].replace("&nfy=1", "")
        request_id = redirect_url.split("id=")[-1]
        await self.session.get(f"{BING_URL}{redirect_url}")
        # https://www.bing.com/images/create/async/results/{ID}?q={PROMPT}
        polling_url = f"{BING_URL}/images/create/async/results/{request_id}?q={url_encoded_prompt}"
        # Poll for results
        if not self.quiet:
            print("Waiting for results...")
        while True:
            if not self.quiet:
                print(".", end="", flush=True)
            # By default, timeout is 300s, change as needed
            response = await self.session.get(polling_url)
            if response.status != 200:
                raise Exception("Could not get results")
            content = await response.text()
            if content:
                break

            await asyncio.sleep(1)
            continue
        # Use regex to search for src=""
        image_links = regex.findall(r'src="([^"]+)"', content)
        # Remove size limit
        normal_image_links = [link.split("?w=")[0] for link in image_links]
        # Remove duplicates
        normal_image_links = list(set(normal_image_links))

        # Bad images
        bad_images = [
            "https://r.bing.com/rp/in-2zU3AJUdkgFe7ZKv19yPBHVs.png",
            "https://r.bing.com/rp/TX9QuO3WzcCJz1uaaSwQAz39Kb0.jpg",
        ]
        for im in normal_image_links:
            if im in bad_images:
                raise Exception("Bad images")
        # No images
        if not normal_image_links:
            raise Exception("No images")
        return normal_image_links

    async def save_images(self, links: list, output_dir: str) -> None:
        """
        Saves images to output directory
        """
        if not self.quiet:
            print("\nDownloading images...")
        with contextlib.suppress(FileExistsError):
            os.mkdir(output_dir)
        try:
            for image_num, link in enumerate(links):
                async with self.session.get(link, raise_for_status=True) as response:
                    # save response to file
                    with open(f"{output_dir}/{image_num}.jpeg", "wb") as output_file:
                        async for chunk in response.content.iter_chunked(8192):
                            output_file.write(chunk)
        except aiohttp.client_exceptions.InvalidURL as url_exception:
            raise Exception(
                "Inappropriate contents found in the generated images. Please try again or try another prompt."
            ) from url_exception


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
        "--quiet",
        help="Disable pipeline messages",
        action="store_true",
    )
    parser.add_argument(
        "--asyncio",
        help="Run ImageGen using asyncio",
        action="store_true",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the version number",
    )
    args = parser.parse_args()

    if args.version:
        print(pkg_resources.get_distribution("BingImageCreator").version)
        sys.exit()

    # Load auth cookie
    with contextlib.suppress(Exception):
        with open(args.cookie_file, encoding="utf-8") as file:
            cookie_json = json.load(file)
            for cookie in cookie_json:
                if cookie.get("name") == "_U":
                    args.U = cookie.get("value")
                    break

    if args.U is None and args.cookie_file is None:
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
