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
ids = [1, 2, 4, 21, 22, 26, 27, 28]

crns = {
     1: {"remotepattern": "up1_Data*.001*.txt",
         "sdpattern": "*.001",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2"]},

     2: {"remotepattern": "up2_Data*.002*.txt",
         "sdpattern": "*.002",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1"]
        },

     4: {"remotepattern": "up4_Data*.004*.txt",
         "sdpattern": "*.004",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt",
                      "counts1", "nsecs1", "counts2", "nsecs2", "MetOne092_1","press4","temp_ext",
                      "relhum_ext","N1T_C","N1RH","N2T_C","N2RH"]
        },

    21: {"remotepattern": "CRSProbe_Data*.021*.txt",
          "sdpattern": "*.021",
          "colnames": ["rec_id", "datetime", "press1", "press4", "temp1","relhum1", "temp_ext",
                       "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH"]
        },

    22: {"remotepattern": "CRSProbe_Data*.022*.txt",
         "sdpattern": "*.022",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1","relhum1", "temp_ext",
                       "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH"]
        },

    26: {"remotepattern": "up26_Data*.026*.txt",
         "sdpattern": "*.026",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2"]
        },

    27: {"remotepattern": "up27_Data*.027*.txt",
         "sdpattern": "*.027",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1",
                      "volt", "counts1", "nsecs1", "counts2", "nsecs2"]
        },

    28: {"remotepattern": "sonde28_Data_*.028*",
         "sdpattern": "*.028",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "volt", "counts1", "nsecs1", "temp2", "relhum2"]
        }
}


for i, id in enumerate(ids):
    print("-------------")
    print("Processing %d" % id)

    try:
        os.remove(tmpfile)
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

    # MERGE
    df = pd.read_csv(tmpfile, sep=",", comment="#", header=None, error_bad_lines=False, warn_bad_lines=True)
    df.columns = crns[id]["colnames"]
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
