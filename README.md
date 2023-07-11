Example use
```sh
$ ./run.sh \
  https://www.cs.uoregon.edu/research/summerschool/summer23/_videos/Petrisan1_1.mp4 \
  https://www.cs.uoregon.edu/research/summerschool/summer23/_videos/Petrisan1_2.mp4 \
  https://www.cs.uoregon.edu/research/summerschool/summer23/_videos/Petrisan1_3.mp4
```

Generate `outline.txt` after spamming OpenAI's whisper and gpt3.5-turbo api.

Note: Sending multiple large requests to whisper and gpt3.5-turbo can get expensive so keep an eye on your account usage.