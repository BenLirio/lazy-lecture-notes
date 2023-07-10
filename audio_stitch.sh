#!/bin/bash

paths=("$@")

file_paths=()
# download url paths
for path in "${paths[@]}"; do
  if [[ $path == http* ]]; then
    local_path=`basename $path`
    if [ -f $local_path ]; then
      echo "ERROR: \"$local_path\" already exists."
      exit 1
    else
      curl -O "$path"
      file_paths+=("$local_path")
    fi
  else
    file_paths+=("$path")
  fi
done



audio_file_paths=()
for file_path in "${file_paths[@]}"; do
  extension="${file_path##*.}"
  if [ $extension != "mp3" ]; then
    if [ $extension == "mp4" ]; then
      file_path_without_extension="${file_path%.*}"
      audio_file_path=$file_path_without_extension.mp3
      ffmpeg -i $file_path $audio_file_path
      rm $file_path
      audio_file_paths+=("$audio_file_path")
    else
      echo "If file is not mp3 it must be mp4"
      exit 1
    fi
  else
    audio_file_paths+=("$file_path")
  fi
done

output_file_name=audio_stitch.mp3

audio_files_file_name=audio_files.txt
for audio_file_path in "${audio_file_paths[@]}"; do
  echo "file '$audio_file_path'" >> $audio_files_file_name
done

ffmpeg -f concat -safe 0 -i $audio_files_file_name -c copy $output_file_name

rm $audio_files_file_name
for audio_file_path in "${audio_file_paths[@]}"; do
  rm $audio_file_path
done

