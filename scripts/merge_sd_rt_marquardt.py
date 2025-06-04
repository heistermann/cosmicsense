# coding: utf-8

import glob
import os
import pandas as pd
import numpy as np
import shutil
from pathlib import Path

sddir = "/home/maik/b2drop/cosmicsense/inbox/marquardt/timeseries/crns/sd"
remotedir = "/home/maik/b2drop/cosmicsense/inbox/marquardt/timeseries/crns/remote"
trgdir = "/media/x/cosmicsense/data/marquardt/crns"
tmpfile = "tmpfile.txt"
tmpfile2 = "tmpfile2.txt"
tmpfile3 = "tmpfile3.txt"
ids = [1, 2, 4, 21, 22, 26, 27, 28]

crns = {
     1: {"remotepattern": "up1_Data*.001*.txt",
         "sdpattern": "*.001",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2"],
         "colnames2": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1","counts2", "nsecs2", "sdiAdr","sdi1_1","sdi1_2","sdi1_3","sdi1_4"]
        },

     2: {"remotepattern": "up2_Data*.002*.txt",
         "sdpattern": "*.002",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1"],
         "colnames2": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1","sdiAdr","sdi1_1","sdi1_2","sdi1_3","sdi1_4","sdi1_5","sdi1_6"]
        },

     4: {"remotepattern": "up4_Data*.004*.txt",
         "sdpattern": "*.004",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt",
                      "counts1", "nsecs1", "counts2", "nsecs2", "MetOne092_1","press4","temp_ext",
                      "relhum_ext","N1T_C","N1RH","N2T_C","N2RH"],
         "colnames2": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt",
                      "counts1", "nsecs1", "counts2", "nsecs2", "MetOne092_1","press4","temp_ext",
                      "relhum_ext","N1T_C","N1RH","N2T_C","N2RH","sdiAdr","sdi2_1","sdi2_2","sdi2_3","sdi2_4"]
        },

    21: {"remotepattern": "CRSProbe_Data*.021*.txt",
          "sdpattern": "*.021",
          "colnames": ["rec_id", "datetime", "press1", "press4", "temp1","relhum1", "temp_ext",
                       "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH"],
          "colnames2": ["rec_id", "datetime", "press1", "press4", "temp1","relhum1", "temp_ext",
                       "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH","sdiAdr","sdi1_1","sdi1_2","sdi1_3","sdi1_4","sdi1_5","sdi1_6"]
        },

    22: {"remotepattern": "CRSProbe_Data*.022*.txt",
         "sdpattern": "*.022",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1","relhum1", "temp_ext",
                       "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH"],
         "colnames2": ["rec_id", "datetime", "press1", "press4", "temp1","relhum1", "temp_ext",
                       "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH","sdiAdr","sdi1_1","sdi1_2","sdi1_3","sdi1_4","sdi1_5","sdi1_6"],
         "colnames3": ["rec_id", "datetime", "press1", "press4", "temp1","relhum1", "temp_ext",
                       "relhum_ext", "volt", "countsloc1", "nsecsloc1", "counts1", "nsecs1", "N1T_C", "N1RH","sdiAdrloc1","sdiloc1_1","sdiloc1_2","sdiloc1_3","sdiloc1_4","sdiAdr","sdi1_1","sdi1_2","sdi1_3","sdi1_4","sdi1_5","sdi1_6"]
        },

    26: {"remotepattern": "up26_Data*.026*.txt",
         "sdpattern": "*.026",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2"]
        },

    27: {"remotepattern": "up27_Data*.027*.txt",
         "sdpattern": "*.027",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1",
                      "volt", "counts1", "nsecs1", "counts2", "nsecs2"],
         "colnames2": ["rec_id", "datetime", "press1", "temp1", "relhum1",
                      "volt", "counts1", "nsecs1", "counts3", "nsecs3", "counts2", "nsecs2"]

        },

    28: {"remotepattern": "sonde28_Data_*.028*",
         "sdpattern": "*.028",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "volt", "counts1", "nsecs1", "temp2", "relhum2"],
         "colnames2": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "volt", "counts1", "nsecs1", "temp2", "relhum2","sdiAdr","sdi1_1","sdi1_2","sdi1_3","sdi1_4"]
        }
}


for i, id in enumerate(ids):
    print("-------------")
    print("Processing %d" % id)

    try:
        os.remove(tmpfile)
        os.remove(tmpfile2)
    except:
        pass

    # REMOTE FILES
    print("Remote: ", end="")
    searchdir = os.path.join(remotedir,"%d" % id, crns[id]["remotepattern"])
    remotefiles = glob.glob(searchdir, recursive=True)
    print("found %d files" % len(remotefiles))

    for name in remotefiles:
        print(".", end="")
        fin = open(name, "r")
        body = fin.read()
        # replace comment character
        body = body.replace("//", "#")
        # replace zombie line endings
        body = body.replace(",\r\n", "\r\n")
        # comment out these lines
        body = body.replace("CRS#1:", "#CRS#1")
        body = body.replace("CRS#2:", "#CRS#2")
        myfile = open(tmpfile, 'a')
        myfile.write(body)
        myfile.close()
    print("")

    # SD
    print("SD: ", end="")
    searchdir = os.path.join(sddir, "%d" % id)
    sdfiles = [filename for filename in Path(searchdir).glob("**/"+crns[id]["sdpattern"])]
    print("found %d files" % len(sdfiles))

    for name in sdfiles:
        print(".", end="")
        fin = open(name, "r")
        body = fin.read()
        # replace comment character
        body = body.replace("//", "#")
        # replace zombie line endings
        body = body.replace(",\r\n", "\r\n")
        body = body.replace(",\n", "\n")
        # comment out these lines
        body = body.replace("CRS#1:", "#CRS#1")
        body = body.replace("CRS#2:", "#CRS#2")
        myfile = open(tmpfile, 'a')
        myfile.write(body)
        myfile.close()
    print("")

    if ("colnames2" in crns[id].keys()) or ("colnames3" in crns[id].keys()):
        # Read all lines. potentially varying no of columns
        myfile = open(tmpfile, 'r')
        lines = myfile.readlines()
        myfile.close()
        # Write in seperate files
        myfile = open(tmpfile, 'w')
        myfile2 = open(tmpfile2, 'w')
        myfile3 = open(tmpfile3, 'w')
        for line in lines:
            split = line.split(",")
            if len(split)==len(crns[id]["colnames"]):
                myfile.write(line+"\n")
            if len(split)==len(crns[id]["colnames2"]):
                myfile2.write(line+"\n")
            try:
                if len(split)==len(crns[id]["colnames3"]):
                    myfile3.write(line+"\n")
            except:
                pass
        myfile.close()
        myfile2.close()
        try:
            myfile3.close()
        except:
            pass

    # MERGE
    df = pd.read_csv(tmpfile, sep=",", comment="#", header=None, error_bad_lines=False, warn_bad_lines=True)
    df.columns = crns[id]["colnames"]
    if "colnames2" in crns[id].keys():
        try:
            df2 = pd.read_csv(tmpfile2, sep=",", comment="#", header=None,
                             error_bad_lines=False, warn_bad_lines=True)
            df2.columns = crns[id]["colnames2"]
            df = df2.append(df, sort=False)
        except:
            print("Problem in reading or appending data with diffferent column scenario")
            raise
    if "colnames3" in crns[id].keys():
        try:
            df3 = pd.read_csv(tmpfile3, sep=",", comment="#", header=None,
                             error_bad_lines=False, warn_bad_lines=True)
            df3.columns = crns[id]["colnames3"]
            df = df3.append(df, sort=False)
        except:
            print("Problem in reading or appending data with diffferent column scenario")
            raise
    df.datetime = pd.to_datetime(df.datetime, format="%Y/%m/%d %H:%M:%S")
    df = df.set_index("datetime")
    df.insert(loc=1, column="datetime", value=df.index)
    df = df.sort_index()
    df = df[df.index >= "2019-07-25"]
    dupl = df.index.duplicated(keep='first')
    if np.any(dupl):
        print("Contains %d duplicates" % len(np.where(dupl)[0]))
        df = df[~dupl]
    fpath = os.path.join(trgdir, "%d/%d_CRNS.txt" % (id, id) )
    df.to_csv(fpath, sep="\t", index=False, date_format="%Y-%m-%d %H:%M:%S")
    print("")
