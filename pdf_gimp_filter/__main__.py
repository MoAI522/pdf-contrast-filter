import os
from re import L
import shutil
import sys
import mimetypes
from pathlib import Path
from time import time
import pdf2image
import cv2
import numpy as np
import img2pdf
from PIL import Image
import toml


def load_config():
    config_path = "./config.toml"
    config = {}
    if (not os.path.exists(config_path)):
        print("config.toml is not found.")
        return None, True
    with open(config_path) as f:
        config = toml.load(f)
    return config, False


def pdf_to_jpeg(input_path):
    dump_path = Path("./dump")
    os.mkdir(dump_path)
    dump_img_folder_path = dump_path / "img"
    os.mkdir(dump_img_folder_path)
    dump_input_pdf_path = dump_path / "input.pdf"
    shutil.copy(input_path, dump_input_pdf_path)

    pdf2image.convert_from_path(
        dump_input_pdf_path,
        output_folder=dump_img_folder_path,
        fmt="jpeg",
        dpi=600,
        output_file="dump.pdf",
        grayscale=True)

    return dump_path, dump_img_folder_path


def process(dump_img_folder_path, alpha, beta):
    for file in dump_img_folder_path.iterdir():
        print("processing: %s" % (file))
        src = cv2.imread(str(file))
        dst = alpha * src + beta
        dst = np.clip(dst, 0, 255).astype(np.uint8)
        cv2.imwrite(str(file), dst)


def save(output_path, dump_img_folder_path):
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert([Image.open(image_path).filename for image_path in sorted(
            dump_img_folder_path.iterdir(), key=lambda path: int(path.stem[-1]))]))


def main():
    config, err = load_config()
    if (err):
        return
    for pdf_path in Path(config["path"]["input_dir"]).iterdir():
        if not pdf_path.is_file() or mimetypes.guess_type(
                str(pdf_path))[0] != "application/pdf":
            continue
        output_path = Path(config["path"]["output_dir"]) / pdf_path.name
        print('"%s" -> "%s"' % (pdf_path, output_path))
        starttime = time()
        dump_path, dump_img_folder_path = pdf_to_jpeg(pdf_path)
        process(
            dump_img_folder_path,
            config["properties"]["alpha"],
            config["properties"]["beta"])
        save(output_path, dump_img_folder_path)
        for image_path in dump_img_folder_path.iterdir():
            os.remove(image_path)
        os.rmdir(dump_img_folder_path)
        for dump_file_path in dump_path.iterdir():
            os.remove(dump_file_path)
        os.rmdir(dump_path)
        os.remove(pdf_path)
        endtime = time()
        print("Done in %dms" % ((endtime - starttime) * 1000,))
        print("--------------------------------------\n")


if __name__ == "__main__":
    main()
