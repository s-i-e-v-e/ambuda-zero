"""
Extract image from PDF
"""
import time
import os


import httpx
import pypdf

import task_exec

class PDFMessage:
    action: str

    file_path: str
    callback: str
    pages: str

    message: str
    page_count: int
    time_taken: int
    images: list[bytes]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def __get_dir_path(x: str):
    xs = x.split(os.sep)
    xs.pop()
    return os.sep.join(xs)


def __encode(xs: bytes) -> str:
    import base64
    ys = base64.b64encode(xs)
    return ys.decode("ascii")

def __random_string():
    import random, string
    length = 16
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def __post_result(result: PDFMessage, start: int):
    end = int(time.perf_counter())
    time_taken = (end - start) // 1_000_000
    result.time_taken = time_taken

    print("posting to" + result.callback)
    x = httpx.post(result.callback, data=vars(result))
    print(f'response: {x.status_code} ({x.text})')


def __get_page_count(p: PDFMessage):
    def fn(p: PDFMessage):
        start = int(time.perf_counter())
        r = pypdf.PdfReader(p.file_path)
        n = len(r.pages)
        p.page_count = n
        __post_result(p, start)


    print("getting-page-count")
    task_exec.exec(fn, p)


def __get_page_image(p: PDFMessage):
    def fn(p: PDFMessage):
        start = int(time.perf_counter())
        r = pypdf.PdfReader(p.file_path)
        xs = p.pages.split('-')
        pages = range(int(xs[0]), int(xs[1]) + 1) if len(xs) > 1 else [int(xs[0])]

        result = PDFMessage()
        result.callback = p.callback
        result.images = list()
        rnd = __random_string()
        for p_page in pages:
            page = r.pages[p_page]

            for count, image_file_object in enumerate(page.images):
                print(f"count: {count}, name: {image_file_object.name}")
                fn = f'/tmp/py_uvi/images/{rnd}_{count}_{image_file_object.name}'
                result.images.append(fn)
                with open(fn, "wb") as fp:
                    fp.write(image_file_object.data)

        result.message = "Image(s) extracted successfully!"
        #d = __get_dir_path(p.file_path)
        #subprocess.run(['pdfimages', p.file_path, p.prefix], cwd=d)
        __post_result(result, start)

    print("getting-page-image")
    task_exec.exec(fn, p)


async def run(a: dict):
    p = PDFMessage(**a)
    if p.action == "get-page-image":
        __get_page_image(p)
    elif p.action == "get-page-count":
        __get_page_count(p)
    else:
        raise ValueError(f"Unknown action: {p.action}")
    return {
        "message": "accepted"
    }