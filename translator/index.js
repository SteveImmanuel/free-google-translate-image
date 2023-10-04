import argparse from 'argparse';
import clipboard from 'clipboardy';
import { firefox } from 'playwright-firefox';
import fs from 'fs';

const translateEmulate = async (imgPath, outPath = '', sourceLang = 'auto', targetLang = 'en') => {
    if (!fs.existsSync(imgPath)) {
        console.error('Input image does not exist');
        process.exit(2);
    }

    let browser;
    let context;

    let translatedText = '';
    let translatedPath = '';

    try {
        const oldClipboardContent = await clipboard.read();

        browser = await firefox.launch({
            headless: false,
            permissions: ['clipboard-read', 'clipboard-write'],
        });
        context = await browser.newContext();
        const page = await context.newPage();
        await page.goto(`https://translate.google.com/?sl=${sourceLang}&tl=${targetLang}&op=images`);
        await page.waitForLoadState('domcontentloaded');

        await page.getByRole('textbox', { name: 'Browse your files' }).setInputFiles(imgPath);

        // some happy coincidence this also waits for the translation to finish
        // need to investigate further
        await page.getByRole('button', { name: 'Copy text' }).click();
        translatedText = await clipboard.read();
        await clipboard.write(oldClipboardContent);

        const regexPattern = /^blob:https:\/\/translate\.google\.com\/.*$/;
        const matchingImages = page.locator('img').filter(async (img) => {
            const srcAttribute = await img.getAttribute('src');
            return regexPattern.test(srcAttribute);
        });

        const image = matchingImages.last();
        const imageData = await image.evaluate(element => {
            let cnv = document.createElement('canvas');
            cnv.width = element.naturalWidth;
            cnv.height = element.naturalHeight;
            cnv.getContext('2d').drawImage(element, 0, 0, element.naturalWidth, element.naturalHeight);
            return cnv.toDataURL().substring(22)
        });
        if (outPath === '') {
            let filename = imgPath.split('/').pop().split('.').slice(0, -1).join('.');
            if (process.platform === 'win32') {
                outPath = `C:\\Users\\${process.env.USERNAME}\\AppData\\Local\\Temp\\${filename}_${targetLang}.png`;
            } else {
                outPath = `/tmp/${filename}_${targetLang}.png`;
            }
        }
        fs.writeFileSync(outPath, imageData, 'base64');
        translatedPath = outPath;
    } catch (error) {
        console.error(error);
    } finally {
        if (context) {
            await context.close();
        }
        if (browser) {
            await browser.close();
        }
    }

    if (translatedText === '' || translatedPath === '') {
        process.exit(1);
    }
    return { translatedText, translatedPath };
};

const parser = argparse.ArgumentParser({
    description: 'Instantly translate an image and outputs the detected texts',
});
parser.add_argument('-i', { help: 'Path to the input image to translate', required: true });
parser.add_argument('-o', { help: 'Path to the output image to save', required: false, default: '' });
parser.add_argument('-sl', { help: 'Source language', required: false, default: 'auto' });
parser.add_argument('-tl', { help: 'Target language', required: false, default: 'en' });

const args = parser.parse_args();
translateEmulate(args.i, args.o, args.sl, args.tl).then(({ translatedText, translatedPath }) => {
    console.log(translatedText);
    console.log(translatedPath);
});