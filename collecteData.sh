#BEGINS THE DATA COLLECTION FROM THE CAMERA
sudo ./Desktop/Doorfly/LeptonUnnormalized/Lepton-CaptureRaw/raspberrypi_video & python Desktop/Doorfly/Keylogger/keylogger.py $1'40'

#RENAMES THE FILES AFTER DATA HAS BEEN COLLECTED
mv pixelValues.txt $1'40UpperRawData.txt'
