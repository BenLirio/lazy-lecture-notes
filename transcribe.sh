#!/bin/sh

file_path=$1
extension="${file_path##*.}"
if [ $extension != "mp3" ]; then
  echo "File must be an mp3"
  exit 1
fi

job_name=`basename $file_path .$extension`-`date +%N`
file_name=$job_name.$extension

cp $file_path $file_name

aws s3 cp \
  $file_name \
  s3://$LAZY_LECTURE_NOTES_BUCKET

rm $file_name

aws transcribe start-transcription-job \
  --transcription-job-name $job_name \
  --language-code en-US \
  --media-format mp3 \
  --media MediaFileUri=s3://$LAZY_LECTURE_NOTES_BUCKET/$file_name \
  --output text \
  --output-bucket-name $LAZY_LECTURE_NOTES_BUCKET

output_file_name=$job_name.json

while true
do
  if aws transcribe get-transcription-job \
    --transcription-job-name $job_name \
    --query 'TranscriptionJob.TranscriptionJobStatus' | grep -q 'IN_PROGRESS';
  then
    echo "Transcription in progress..."
    sleep 1
  else
    echo "Transcription complete"
    break
  fi
done


aws s3 rm s3://$LAZY_LECTURE_NOTES_BUCKET/$file_name
aws s3 cp s3://$LAZY_LECTURE_NOTES_BUCKET/$output_file_name .
aws s3 rm s3://$LAZY_LECTURE_NOTES_BUCKET/$output_file_name


transcript_file_name=$job_name.txt

cat $output_file_name | jq -r '.results.transcripts[].transcript' > $transcript_file_name
rm $output_file_name