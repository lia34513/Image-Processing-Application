#!/usr/bin/env bash
cd frontend;
yarn
yarn build
yarn autobuild &
cd ../;
python -u server.py;
