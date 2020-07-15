# coding: utf-8

import glob
import os
import pandas as pd
import numpy as np
import shutil
from pathlib import Path

sddir = "/media/x/cosmicsense/data/sponheim_rhinluch/sd"
remotedir = "/media/x/cosmicsense/data/sponheim_rhinluch/remote"
trgdir = "/media/x/cosmicsense/data/sponheim_rhinluch/merged"
tmpfile = "tmpfile.txt"
tmpfile2 = "tmpfile2.txt"
ids = ["spo", "rhi"]

crns = {
     "spo": {"remotepattern": "sponheim_Data_*.spo_*.txt",
         "sdpattern": "na",
         "colnames": ["rec_id", "datetime", "press4", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "temp2", "relhum2", "sdiAdr", "sdi1_1", "sdi1_2", "sdi1_3", "sdi1_4", "sdi1_5", "sdi1_6"],
        },

     "rhi": {"remotepattern": "rhinluch_Data*.rhi_*.txt",
         "sdpattern": "na",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "sdiAdr", "sdi1_1", "sdi1_2", "sdi1_3", "sdi1_4"],
        }
}

for i, id in enumerate(ids):
    print("-------------")
    print("Processing %s" % id)

    try:
        os.remove(tmpfile)
        os.remove(tmpfile2)
    except:
        pass

    # REMOTE FILES
    print("Remote: ", end="")
    searchdir = os.path.join(remotedir,"%s" % id, crns[id]["remotepattern"])
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
    searchdir = os.path.join(sddir, "%s" % id)
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

    if "colnames2" in crns[id].keys():
        # Read all lines. potentially varying no of columns
        myfile = open(tmpfile, 'r')
        lines = myfile.readlines()
        myfile.close()
        # Write in seperate files
        myfile = open(tmpfile, 'w')
        myfile2 = open(tmpfile2, 'w')
        for line in lines:
            split = line.split(",")
            if len(split)==len(crns[id]["colnames"]):
                myfile.write(line+"\n")
            if len(split)==len(crns[id]["colnames2"]):
                myfile2.write(line+"\n")
        myfile.close()
        myfile2.close()

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
    df.datetime = pd.to_datetime(df.datetime, format="%Y/%m/%d %H:%M:%S")
    df = df.set_index("datetime")
    df.insert(loc=1, column="datetime", value=df.index)
    df = df.sort_index()
    df = df[df.index >= "2019-07-25"]
    dupl = df.index.duplicated(keep='first')
    if np.any(dupl):
        print("Contains %d duplicates" % len(np.where(dupl)[0]))
        df = df[~dupl]
    fpath = os.path.join(trgdir, "%s_CRNS.txt" % id )
    df.to_csv(fpath, sep="\t", index=False, date_format="%Y-%m-%d %H:%M:%S")
    print("")
