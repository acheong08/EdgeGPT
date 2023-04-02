<a id="ImageGen"></a>

# ImageGen

<a id="ImageGen.ImageGen"></a>

## ImageGen Objects

```python
class ImageGen()
```

Image generation by Microsoft Bing

**Arguments**:

- `auth_cookie` - str

<a id="ImageGen.ImageGen.get_images"></a>

#### get\_images

```python
def get_images(prompt: str) -> list
```

Fetches image links from Bing

**Arguments**:

- `prompt` - str

<a id="ImageGen.ImageGen.save_images"></a>

#### save\_images

```python
def save_images(links: list, output_dir: str) -> None
```

Saves images to output directory

