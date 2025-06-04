# coding: utf-8

import glob
import os
import pandas as pd
import numpy as np
import shutil
from pathlib import Path
import sys

#sddir = "/home/maik/b2drop/cosmicsense/inbox/marquardt/timeseries/crns/sd"
remotedir = "/home/maik/b2drop/cosmicsense/inbox/wuestebach/timeseries/crns/JFC-2"
trgdir = "/home/maik/b2drop/cosmicsense/inbox/wuestebach/timeseries/crns/merged"
tmpfile = "tmpfile.txt"
#tmpfile2 = "tmpfile2.txt"
#tmpfile3 = "tmpfile3.txt"
#ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
#ids = [10,11]
ids = eval(sys.argv[1])

crns = {
     1: {"remotepattern": "fzj01_Data.txt",
         "sdpattern": "*.001",
         #"colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"]
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "volt", "counts1", "counts2", "nsecs1", "nsecs2", "bug1"]
        },

     2: {"remotepattern": "fzj02_Data.txt",
         "sdpattern": "*.002",
         #"colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"]
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "volt", "counts1", "counts2", "nsecs1", "nsecs2", "unknown1", "unknown2", "unknown3", "unknown4", "bug1"]
        },

     3: {"remotepattern": "fzj03_Data.txt",
         "sdpattern": "*.002",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"]
        },

     4: {"remotepattern": "fzj04_Data.txt",
         "sdpattern": "*.004",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"]
        },

     5: {"remotepattern": "fzj05_Data.txt",
         "sdpattern": "*.002",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"]
        },

     6: {"remotepattern": "fzj06_Data.txt",
         "sdpattern": "*.002",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"]
        },

     7: {"remotepattern": "07_Data_*.007_*.txt",
         "sdpattern": "*.007",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp2", "relhum2"]
        },

     8: {"remotepattern": "up08_Data_*.008_*.txt",
         "sdpattern": "*.008",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "volt", "counts1", "nsecs1"]
        },

     9: {"remotepattern": "up09_Data_*.009_*.txt",
         "sdpattern": "*.009",
            "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2"]
        },

     10: {"remotepattern": "kit10_Data.txt",
         "sdpattern": "*.002",
         "colnames": ["rec_id","datetime","press4","press1","temp1","relhum1","temp_ext","relhum_ext","volt","counts1","counts2","nsecs1","nsecs2","N1T_C","N1RH","N2T_C","N2RH"]
        },

     11: {"remotepattern": "kit11_Data.txt",
         "sdpattern": "*.002",
         "colnames": ["rec_id","datetime","press4","press1","temp1","relhum1","temp_ext","relhum_ext","volt","counts1","counts2","nsecs1","nsecs2","N1T_C","N1RH","N2T_C","N2RH"]
        },

     12: {"remotepattern": "CRSProbe_Data_*.830_*.txt",
         "sdpattern": "*.002",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "temp_ext", "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH"]
        },

     13: {"remotepattern": "CRSProbe_Data*.13_*.txt",
         "sdpattern": "*.013",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "temp_ext", "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH"]
        },

     14: {"remotepattern": "CRSProbe_Data*.14_*.txt",
         "sdpattern": "*.014",
         "colnames": ["rec_id", "datetime", "press1", "press4", "temp1", "relhum1", "temp_ext", "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH"]
        },

     15: {"remotepattern": "fzj15_Data.txt",
         "sdpattern": "*.002",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"]
        }
}


for i, id in enumerate(ids):
    print("-------------")
    print("Processing %d" % id)

    try:
        os.remove(tmpfile)
        print("REMOVED: %s" % tmpfile )
    except FileNotFoundError:
        pass

    # REMOTE FILES
    print("Remote: ", end="")
    searchdir = os.path.join(remotedir,"%d" % id, crns[id]["remotepattern"])
    remotefiles = glob.glob(searchdir, recursive=True)
    print("found %d files" % len(remotefiles))

    if len(remotefiles)==0:
        continue

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

#     # SD
#     print("SD: ", end="")
#     searchdir = os.path.join(sddir, "%d" % id)
#     sdfiles = [filename for filename in Path(searchdir).glob("**/"+crns[id]["sdpattern"])]
#     print("found %d files" % len(sdfiles))

#     for name in sdfiles:
#         print(".", end="")
#         fin = open(name, "r")
#         body = fin.read()
#         # replace comment character
#         body = body.replace("//", "#")
#         # replace zombie line endings
#         body = body.replace(",\r\n", "\r\n")
#         body = body.replace(",\n", "\n")
#         # comment out these lines
#         body = body.replace("CRS#1:", "#CRS#1")
#         body = body.replace("CRS#2:", "#CRS#2")
#         myfile = open(tmpfile, 'a')
#         myfile.write(body)
#         myfile.close()
#     print("")

    # MERGE
    df = pd.read_csv(tmpfile, sep=",", comment="#", header=None, error_bad_lines=False, warn_bad_lines=True)
    df.columns = crns[id]["colnames"]
    # get rid of NA columns
    df = df.iloc[~(np.array(df.isnull().sum(axis=1).tolist())>4),:]
    #print( len(np.where(df.datetime.isna())[0]) )
    df.datetime = pd.to_datetime(df.datetime, format="%Y/%m/%d %H:%M:%S", errors="coerce")
    df = df[~df.datetime.isna()]
    df = df.set_index("datetime")
    df.insert(loc=1, column="datetime", value=df.index)
    df = df.sort_index()
    #df = df[df.index >= "2019-07-25"]
    dupl = df.index.duplicated(keep='first')
    if np.any(dupl):
        #print("Contains %d duplicates" % len(np.where(dupl)[0]))
        print(np.where(dupl)[0])
        df = df[~dupl]
    fpath = os.path.join(trgdir, "%d_CRNS.txt" % id )
    df.to_csv(fpath, sep="\t", index=False, date_format="%Y-%m-%d %H:%M:%S")
    print("")
