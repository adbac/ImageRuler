from pathlib import Path

import click
from drawBot import *
from drawBotGrid import verticalAlignTextBox
from pypdf import PdfReader, PdfWriter
import subprocess


def centimeters(points):
    return points * 2.54 / 72

def points(centimeters):
    return centimeters * 72 / 2.54


@click.command()
@click.argument("srcfile", nargs=1, type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True))
@click.argument("outdir", nargs=1, type=click.Path(file_okay=False, dir_okay=True))
@click.option("-s", "--suffix", default="_ruled", nargs=1, help="The suffix to add to the filename for distinction purposes.")
@click.option("-o", "--overwrite", is_flag=True, help="Overwrite existing files.")

def ruleImage(srcfile, outdir, suffix="_ruled", overwrite=False):
    """
    Takes a PDF file and makes a JPG image with the first page of the file
    and a ruler on its left side indicating the height of the page's size.
    """

    newDrawing()

    outdir = Path(outdir)
    srcfile = Path(srcfile)
    outPath = outdir / (srcfile.stem + suffix + ".jpg")
    pageNb = 0  # zero-based index

    if outPath.exists() and overwrite:
        outPath.unlink()
    elif outPath.exists():
        return

    outdir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(srcfile)
    writer = PdfWriter()
    writer.add_page(reader.pages[pageNb])

    pdfTempPath = outdir / (srcfile.stem + "_temp" + srcfile.suffix)
    with open(pdfTempPath, "wb") as f:
        writer.write(f)

    # LAYOUT VARIABLES
    rulerWidth = 20
    rulerPadRight = 12
    smallMark = 5
    smallStroke = .3
    largeMark = 8
    largeStroke = .4
    padding = 10
    textSize = 4

    # LAYOUT

    width, height = imageSize(pdfTempPath)

    cmWidth = centimeters(width)
    cmHeight = centimeters(height)

    cmUnit = width / cmWidth
    mmUnit = cmUnit / 10

    pageWidth = width + (padding * 2) + rulerWidth + rulerPadRight
    pageHeight = height + (padding * 2)

    newPage(pageWidth, pageHeight)

    fill(0)
    rect(0, 0, pageWidth, pageHeight)

    with savedState():
        x, y = (padding + rulerWidth + rulerPadRight, padding)
        image(pdfTempPath, (x, y))

    x = padding
    y = padding
    stroke(1)
    mmHeight = int(round(cmHeight * 10))
    for mm in range(mmHeight + 1):
        fill(None)
        if mm % 10 == 0 or mm == mmHeight:
            sw = largeStroke
            lineWidth = largeMark
            showText = True if (y < (height + padding - mmUnit) or mm == mmHeight) else False
            displayValue = str(int(round(mm/10)) if mm % 10 == 0 else round(mm/10, 1))
        else:
            sw = smallStroke
            lineWidth = smallMark
            showText = False
        strokeWidth(sw)
        line(
            ((x + rulerWidth - lineWidth), y),
            ((x + rulerWidth), y)
        )
        if showText:
            font("IBMPlexMono-Light" if mm == mmHeight else "IBMPlexMono-Thin")
            fontSize(textSize)
            fill(1)
            verticalAlignTextBox(
                displayValue,
                (x, y - textSize, rulerWidth - lineWidth - 2, textSize * 2),
                "right",
                "center"
            )
        y += mmUnit

    saveImage(outPath, imageResolution=300)
    pdfTempPath.unlink(missing_ok=True)

    print(f"{srcfile} > {outPath}")


@click.command()
@click.argument("srcdir", nargs=1, type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument("outdir", nargs=1, type=click.Path(file_okay=False, dir_okay=True))
@click.option("-s", "--suffix", default="_ruled", nargs=1, help="The suffix to add to the filenames for distinction purposes.")
@click.option("-o", "--overwrite", is_flag=True, help="Overwrite existing files.")

def ruleImages(srcdir, outdir, suffix="_ruled", overwrite=False):
    """
    Calls the `ruleImage` function for every PDF file in a given folder.
    """
    for pdf in Path(srcdir).rglob("*.pdf"):
        args = [
            "rule_image",
            str(pdf),
            str(outdir),
            "-s", suffix,
        ]
        if overwrite:
            args.append("-o")
        subprocess.run(args, check=True)