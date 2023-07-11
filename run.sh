#!/bin/bash
./audio_stitch.sh $@
python3 transcribe.py
python3 outline.py