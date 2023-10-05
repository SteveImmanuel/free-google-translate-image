#!/bin/bash

rm -rf dist build
PLAYWRIGHT_BROWSERS_PATH=0 pyinstaller main.spec
