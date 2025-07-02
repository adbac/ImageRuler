> [!WARNING]
> **This tool only runs on macOS since it depends on the `drawBot` library**

# 📐 Image Ruler

Image Ruler is a Python command-line tool written in May 2025 during an internship at the ANRT (Atelier National de Recherche Typographique). Given a path to a pdf file, it takes its first page and draws a digital ruler on its left side, indicating the image's size. Its main use case is for books or objects digitized at their real size.

It uses the `pypdf` and `drawBot` Python modules to make the image (along with `drawBotGrid`).

## Prerequisites

1. **🐍 Make sure you have Python installed on your computer**
   * Open the Terminal app, type `python` or `python3` > if it displays Python's version and info, you're good.
   * If not, download the latest version here: https://www.python.org/downloads/
2. Install the tool by running `python3 -m pip install git+https://github.com/adbac/ImageRuler` (you can copy/paste)
3. For legibility considerations, the digital ruler was built with a monospace font. You can find it in the `fonts` folder of this repository, download it and install it. You can also choose not to, it will work either way!

## Usage

### `rule_image` • Single PDF mode

Type the following in your terminal:
```shell
rule_image '<pdf-path>' '<images-folder-path>'
```
Where `<pdf-path>` is the path to the PDF file that will be used, and `<images-folder-path>` is the path to the folder the final image will be placed in.

### `rule_images` • Multiple PDF mode

Type the following in your terminal:
```shell
rule_images '<pdf-folder-path>' '<images-folder-path>'
```
Where `<pdf-folder-path>` is the path to the folder containing the PDF files that will be used, and `<images-folder-path>` is the path to the folder the final image will be placed in.

**All paths have to be relative to the current working folder** - You can display it by typing `pwd` in the terminal

---

### More options

#### Filename suffix

All output images are suffixed with "_ruled", but you can change that by specifying your own suffix in the command with `-s 'suffix'`. Example:
```shell
rule_image 'scans/book.pdf' 'images/' -s '_cover'
```
Here, the final image will have the name `book_cover.pdf` instead of `book_ruled.pdf` (which is the default behaviour).

#### Overwriting files

By default, if the final image already exists, the tool skips it. But if you want to overwrite exisiting images with the option `-o`. Example:
```shell
rule_image 'scans/book.pdf' 'images/' -o
```
Here, if the `book_ruled.pdf` file already exists in the `images` folder, it will be overwritten instead of being skipped.