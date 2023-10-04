// const puppeteer = require('puppeteer');

// const startBrowser = async () => {
//     const browser = await puppeteer.launch({
//         headless: false,
//         args: ['--disable-setuid-sandbox', '--no-sandbox'],
//         ignoreHTTPSErrors: true,
//         product: 'firefox',
//     });

//     return browser;
// };

// const translateEmulate = async (imgPath, sourceLang = 'auto', targetLang = 'en', timeout = 3000) => {
//     let translatorBrowser;

//     if (targetLang === sourceLang) {
//         return;
//     }

//     try {
//         translatorBrowser = await startBrowser();
//         let browserPage = await translatorBrowser.newPage();
//         let success = true;

//         await browserPage.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36')

//         await browserPage.goto(
//             `https://translate.google.com`,
//             // `https://translate.google.com/?sl=${sourceLang}&tl=${targetLang}&op=images`,
//             { waitUntil: 'load' },
//         );
//         console.log('ready')

//         // await browserPage.waitForSelector('input#ucj-28');
//         // const uploadButton = await browserPage.$('input#ucj-28');

//         // const [fileChooser] = await Promise.all([
//         //     browserPage.waitForFileChooser(),
//         //     await uploadButton.evaluate(btn => btn.click()),
//         // ]);
//         // await fileChooser.accept([imgPath]);
//         console.log('upload success')
//         await browserPage.waitForTimeout(500000);
//         await browserPage.close();
//     } catch (error) {
//         console.error(error);
//     } finally {
//         if (translatorBrowser) {
//             await translatorBrowser.close();
//         }
//     }
// };

// translateEmulate('/home/steve/Git/screen-translate/translator/a.png', sourceLang = 'kr')

const { firefox } = require('playwright');

(async () => {
    const browser = await firefox.launch({
        headless: false
    });
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.goto('https://translate.google.com');

    console.log('ready')
    await page.getByRole('button', { name: 'Image translation' }).click();
    await page.getByRole('main', { name: 'Image translation' }).locator('label').click();
    await page.getByRole('textbox', { name: 'Browse your files' }).setInputFiles('/home/steve/Git/screen-translate/translator/a.png');

    await new Promise(r => setTimeout(r, 100000));


    // ---------------------
    await context.close();
    await browser.close();
})();