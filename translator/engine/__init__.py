import pyperclip
import os
import sys
import logging
import re
import base64
import tempfile
from typing import List
from playwright.sync_api import sync_playwright, ElementHandle, Browser, BrowserContext, Page, Locator

PATTERN = re.compile(r'^blob:https:\/\/translate\.google\.com\/.*$')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_img(img: ElementHandle):
    img.get_attribute('src')
    return bool(PATTERN.match(img.get_attribute('src')))


def translate_emulate(
    input_path: str,
    out_path: str = '',
    source_lang: str = 'auto',
    target_lang: str = 'en',
    headless: bool = True,
):
    logger.info(f'Translating image {input_path} from {source_lang} to {target_lang}')

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
            browser: Browser = playwright.firefox.launch(headless=headless)
            logger.info('Browser launched')
            context: BrowserContext = browser.new_context()
            logger.info('Context created')
            page: Page = context.new_page()
            logger.info('Page created')
            page.goto(f'https://translate.google.com/?sl={source_lang}&tl={target_lang}&op=images')
            page.wait_for_load_state('domcontentloaded')

            page.get_by_role('textbox', name='Browse your files').set_input_files(input_path)
            logger.info('Input image uploaded')

            page.get_by_role('button', name='copy text').click()
            translated_text = pyperclip.paste()
            imgs: List[Locator] = page.locator('img').all()
            matched_img: ElementHandle = list(filter(find_img, imgs))[-1]
            logger.info('Finding translated image result')

            img_data = matched_img.evaluate('''element => {
                let cnv = document.createElement('canvas');
                cnv.width = element.naturalWidth;
                cnv.height = element.naturalHeight;
                cnv.getContext('2d').drawImage(element, 0, 0, element.naturalWidth, element.naturalHeight);
                return cnv.toDataURL().substring(22)
            }''')
            logger.info('Saving translated image')
            if img_data:
                if out_path == '':
                    ext: str = input_path.split('.')[-1]
                    file, name = tempfile.mkstemp(suffix=f'.{ext}')
                    with os.fdopen(file, 'wb') as f:
                        f.write(base64.b64decode(img_data))
                    translated_path = name
                else:
                    with open(out_path, 'wb') as f:
                        f.write(base64.b64decode(img_data))
                    translated_path = out_path
        except Exception as e:
            sys.stderr.write(f'Error: {e}\n')
        finally:
            if context:
                context.close()
            if browser:
                browser.close()

    pyperclip.copy(old_clipboard)
    return translated_path, translated_text
