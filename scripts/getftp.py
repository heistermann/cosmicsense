import ftplib
import io
import os
import sys

ftpuser = sys.argv[1]
ftppw = sys.argv[2]
trgdir = sys.argv[3]


ftp = ftplib.FTP('irgendwosonst.de')
ftp.login(ftpuser , ftppw)

probes = [1,2,3,4]

for probe in probes:
    print("----------------------")
    print("Processing %d" % probe)
    for file in ftp.nlst('jfc/sonde%d/' % probe):
        fname = os.path.basename(file)
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
