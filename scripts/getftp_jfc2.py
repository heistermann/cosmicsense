import ftplib
import io
import os
import sys

ftpserver = sys.argv[1]
ftpuser = sys.argv[2]
ftppw = sys.argv[3]
trgdir = sys.argv[4]
probes = eval(sys.argv[5])

ftp = ftplib.FTP(ftpserver)
ftp.login(ftpuser , ftppw)


for probe in probes:
    print("----------------------")
    print("Processing %d" % probe)
    subdir = 'wuestebach/sonde%d/' % probe
    if probe==12:
        subdir=""
    for file in ftp.nlst(subdir):
        fname = os.path.basename(file)
        if probe==12:
            if not ".830_" in fname:
                continue
        fpath = os.path.join(trgdir, str(probe), fname)
        if os.path.exists(fpath):
            print("EXISTS: %s" % file)
            continue
        try:
            r = io.BytesIO()
            ftp.retrbinary('RETR ' + file , r.write)
            data = r.getvalue().decode()
            r.close()
            print("SUCCESS: %s" % file)
        except:
            print("FAILED: %s" % file)
            continue
        f = open(fpath , 'w+')
        f.write(data)
        f.close()
ftp.close()
