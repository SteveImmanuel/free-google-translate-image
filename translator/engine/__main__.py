import sys
import argparse
from translator.engine import translate_emulate

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Instantly translate an image and outputs the detected texts')
    parser.add_argument('-i', help='Input image path', required=True, type=str)
    parser.add_argument('-o', help='Output image path', required=False, type=str, default='')
    parser.add_argument('-sl', help='Source language', required=False, type=str, default='auto')
    parser.add_argument('-tl', help='Target language', required=False, type=str, default='en')
    parser.add_argument('-v', help='Launch in non-headless mode', action='store_true')
    args = parser.parse_args()
    print(args)
    translated_path, translated_text = translate_emulate(args.i, args.o, args.sl, args.tl, not args.v)
    if not translated_path or not translated_text:
        sys.stderr.write('Failed to translate image\n')
        sys.exit(1)
    print(translated_path)
    print(translated_text)  # WARNING: copy text not working when in headless mode
