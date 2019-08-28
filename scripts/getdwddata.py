from zipfile import ZipFile
import shutil
import os.path as path
import os
import subprocess


#pressfile = "ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/pressure/recent/stundenwerte_P0_02290_akt.zip"
#tempfile = "ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/air_temperature/recent/stundenwerte_TU_02290_akt.zip"
#precfile = "ftp://ftp-cdc.dwd.de/pub/CDC/observations_germany/climate/hourly/precipitation/recent/stundenwerte_RR_02290_akt.zip"
pressfile = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/pressure/recent/stundenwerte_P0_02290_akt.zip"
tempfile = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/air_temperature/recent/stundenwerte_TU_02290_akt.zip"
precfile = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/hourly/precipitation/recent/stundenwerte_RR_02290_akt.zip"
localdir = "/media/x/cosmicsense/data/fendt/dwd"

def unzip(myzip, mytarget, pattern):
    with ZipFile(path.join(myzip), 'r') as zipObj:
        listOfFileNames = zipObj.namelist()
        for fileName in listOfFileNames:
            if pattern in fileName:
                source = zipObj.open(fileName)
                target = open(mytarget, "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

subprocess.run(["wget", pressfile])
subprocess.run(["wget", tempfile])
subprocess.run(["wget", precfile])

unzip(path.basename(pressfile), path.join(localdir, path.basename(pressfile).strip("zip"))+"txt", "produkt_p0_stunde")
os.remove(path.basename(pressfile))
unzip(path.basename(tempfile), path.join(localdir, path.basename(tempfile).strip("zip"))+"txt", "produkt_tu_stunde")
os.remove(path.basename(tempfile))
unzip(path.basename(precfile), path.join(localdir, path.basename(precfile).strip("zip"))+"txt", "produkt_rr_stunde")
os.remove(path.basename(precfile))
