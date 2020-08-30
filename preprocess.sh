#!/bin/sh
set -e
# possible -i (project path)

while getopts i: option
do
case "${option}"
in
i) PRE_PATH=${OPTARG};;
esac
done
#sudo mkdir $PRE_PATH
#sudo mkdir $PRE_PATH/txtOutput
#sudo mkdir $PRE_PATH/pre_output
echo $PRE_PATH
chmod 777 -R $PRE_PATH
echo Java Process pdf to text
java -jar -Xmx6g ./Tools/PDFtoText.jar $PRE_PATH $PRE_PATH/txtOutput
echo Python Process text files
python ./Tools/preprocess.py -i "$PRE_PATH/txtOutput" -o "$PRE_PATH/pre_output"
