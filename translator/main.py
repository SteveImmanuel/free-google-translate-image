import argparse
import pyperclip
import os
import sys
import re
import base64
import tempfile
from typing import List
from playwright.sync_api import sync_playwright, ElementHandle, Browser, BrowserContext, Page, Locator

PATTERN = re.compile(r'^blob:https:\/\/translate\.google\.com\/.*$')


def find_img(img: ElementHandle):
    img.get_attribute('src')
    return bool(PATTERN.match(img.get_attribute('src')))


def translate_emulate(input_path: str, out_path: str = '', source_lang: str = 'auto', target_lang: str = 'en'):
    if not os.path.exists(input_path):
        sys.stderr.write(f'Input image {input_path} does not exist\n')
        sys.exit(2)

    browser = None
    context = None

    translated_text = None
    translated_path = None

    old_clipboard = pyperclip.paste()

    with sync_playwright() as playwright:
        try:
            firefox = playwright.firefox
            browser: Browser = firefox.launch(headless=True)
            context: BrowserContext = browser.new_context()
            context.grant_permissions(['clipboard-read', 'clipboard-write'])
            page: Page = context.new_page()
            page.goto(f'https://translate.google.com/?sl={source_lang}&tl={target_lang}&op=images')
            page.wait_for_load_state('domcontentloaded')

            page.get_by_role('textbox', name='Browse your files').set_input_files(input_path)
            page.get_by_role('button', name='copy text').click()
            translated_text = pyperclip.paste()

            imgs: List[Locator] = page.locator('img').all()
            matched_img: ElementHandle = list(filter(find_img, imgs))[-1]

            img_data = matched_img.evaluate('''element => {
                let cnv = document.createElement('canvas');
                cnv.width = element.naturalWidth;
                cnv.height = element.naturalHeight;
                cnv.getContext('2d').drawImage(element, 0, 0, element.naturalWidth, element.naturalHeight);
                return cnv.toDataURL().substring(22)
            }''')
            if img_data:
                if out_path == '':
                    ext: str = input_path.split('.')[-1]
                    file, name = tempfile.mkstemp(suffix=f'.{ext}')
                    with os.fdopen(file, 'wb') as f:
                        f.write(base64.b64decode(img_data))
                    translated_path = name
        except Exception as e:
            sys.stderr.write(f'Error: {e}\n')
        finally:
            if context:
                context.close()
            if browser:
                browser.close()

    pyperclip.copy(old_clipboard)
    return translated_path, translated_text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Instantly translate an image and outputs the detected texts')
    parser.add_argument('-i', help='Input image path', required=True, type=str)
    parser.add_argument('-o', help='Output image path', required=False, type=str, default='')
    parser.add_argument('-sl', help='Source language', required=False, type=str, default='auto')
    parser.add_argument('-tl', help='Target language', required=False, type=str, default='en')
    args = parser.parse_args()
    translated_path, translated_text = translate_emulate(args.i, args.o, args.sl, args.tl)
    if not translated_path or not translated_text:
        sys.stderr.write('Failed to translate image\n')
        sys.exit(1)
    print(translated_path)
    print(translated_text)  # WARNING: text not working when in headless mode
