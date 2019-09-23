# coding: utf-8

import glob
import os
import pandas as pd
import numpy as np
import shutil

# BLOCK FOR JFC1 AT FENDT
rootdir = "/home/maik/b2drop/cosmicsense/inbox/fendt/timeseries/crns/JFC-1-sd"
rtdir = "/home/maik/b2drop/cosmicsense/inbox/fendt/timeseries/crns/JFC-1"
trgdir = "/media/x/cosmicsense/data/fendt/crns"
tmpfile = "tmpfile.txt"
id_sd = [5, 6, 14, 18, 19]
id_sd_other = [2, 3, 4, 21, 22, 23]
id_rt = [1, 2, 3, 4, 5, 6, 7, 8, 16, 17, 18, 19, 21, 22, 23, 24, 25]
id_all = [1, 2, 3, 4, 5, 6, 7, 8, 14, 16, 17, 18, 19, 21, 22, 23, 24, 25]

crns = {
#     2: {"pattern": ".002",
#         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1"]
#        },
#
#     3: {"pattern": ".003",
#         "colnames": ["rec_id", "datetime", "press1", "temp1",
#                      "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "T4_C"]
#        },
#
#     4: {"pattern": ".004",
#         "colnames": ["rec_id", "datetime", "press1", "temp1",
#                      "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "T4_C"]
#        },
#    //RecordNum,Date Time(UTC),P1_mb,T1_C,RH1,Vbat,N1Cts,N2Cts,N1ET_sec,N2ET_sec,N1T_C,N1RH,N2T_C,N2RH,MetOne092_1,P4_mb,T_CS215,RH_CS215,

    5: {"pattern": ".005",
         "colnames": ["rec_id", "datetime", "press4", "press1", "temp1",
                      "relhum1", "temp_ext", "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH"]
        },

    6: {"pattern": ".006",
         "colnames": ["rec_id", "datetime", "press4", "press1", "temp1",
                      "relhum1", "temp_ext", "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH"]
        },

    14: {"pattern": ".836",
         "colnames": ["rec_id", "datetime", "press4", "press1", "temp1",
                      "relhum1", "temp_ext", "relhum_ext", "volt", "counts1", "nsecs1", "N1T_C", "N1RH"]
        },

    18: {"pattern": ".018",
         "colnames": ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1",
                       "counts2", "nsecs2", "temp_ext", "relhum_ext"]
        },

    19: {"pattern": ".019",
         "colnames": ["rec_id", "datetime", "press1", "temp1",
                      "relhum1", "volt", "counts1", "nsecs1", "temp_ext", "relhum_ext"]
        }

}


for i, id in enumerate(id_sd):
    crnsdir = os.path.join(rootdir, str(id))
    print(crnsdir)
    if not os.path.exists(crnsdir):
        print("Path not found: %s" % crnsdir)
    try:
        os.remove(tmpfile)
    except:
        pass
    for name in glob.glob(crnsdir+'/**/*'+crns[id]["pattern"], recursive=True):
        print("\t", name)
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
    df = pd.read_csv(tmpfile, sep=",", comment="#", header=None, error_bad_lines=False, warn_bad_lines=True)
    df.columns = crns[id]["colnames"]
    df.datetime = pd.to_datetime(df.datetime, format="%Y/%m/%d %H:%M:%S")
    df = df.set_index("datetime")
    df.insert(loc=1, column="datetime", value=df.index)
    df = df.sort_index()
    df = df[df.index >= "2019-05-01"]
    dupl = df.index.duplicated(keep='first')
    if np.any(dupl):
        print("Contains %d duplicates" % len(np.where(dupl)[0]))
        df = df[~dupl]
    fpath = os.path.join(trgdir, "%d/%d_CRNS.txt" % (id, id) )
    df.to_csv(fpath, sep="\t", index=False, date_format="%Y-%m-%d %H:%M:%S")


# copy the other files from cosmicshare SD directory
for id in id_sd_other:
    print("Copy %d..." % id, end="")
    srcpath = os.path.join(rootdir, "%d/%d_CRNS.txt" % (id, id) )
    trgpath = os.path.join(trgdir, "%d/%d_CRNS.txt" % (id, id) )
    try:
        shutil.copyfile(srcpath, trgpath)
        print("")
    except:
        print("FAILED.")


# copy the real time products
for id in id_rt:
    print("Copy %d..." % id, end="")
    srcpath = os.path.join(rtdir, "%d/%d_CRNS.txt" % (id, id) )
    trgpath = os.path.join(trgdir, "%d/%d_CRNS_rt.txt" % (id, id) )
    try:
        shutil.copyfile(srcpath, trgpath)
        print("")
    except:
        print("FAILED.")


# merge real time and sd products
coll = {}
for id in id_all:
    print("---------------------------------------------------")
    print(id)
    f_rt = os.path.join(trgdir, "%d/%d_CRNS_rt.txt" % (id, id) )
    f_sd = os.path.join(trgdir, "%d/%d_CRNS.txt" % (id, id) )

    try:
        df_rt = pd.read_csv(f_rt, sep="\t")
    except:
        print("No RT product found: %d" % id)
        df_rt = pd.DataFrame()
    else:
        df_rt.datetime = pd.to_datetime(df_rt.datetime)
        df_rt = df_rt.set_index("datetime")
        df_rt = df_rt.rename(index=str, columns={"T_CS215": "temp_ext", "RH_CS215": "relhum_ext"})
        try:
            df_rt = df_rt.drop(columns="id_flag")
        except:
            pass
        try:
            df_rt = df_rt.drop(columns="file_no")
        except:
            pass

    try:
        df_sd = pd.read_csv(f_sd, sep="\t")
    except:
        print("No SD product found: %d" % id)
        df_sd = pd.DataFrame()
    else:
        df_sd.datetime = pd.to_datetime(df_sd.datetime)
        df_sd = df_sd.set_index("datetime")
        df_sd = df_sd.rename(index=str, columns={"T_CS215": "temp_ext", "RH_CS215": "relhum_ext"})
        if id==4:
            df_sd = df_sd.rename(index=str, columns={"MetOne092_1": "press_ext", "N1T_C": "temp_shield1",
                                                    "N1RH": "relhum_shield1", "N2T_C": "temp_shield2",
                                                    "N2RH": "relhum_shield2"})
        try:
            df_sd = df_sd.drop(columns="id_flag")
        except:
            pass
        try:
            df_sd = df_sd.drop(columns="file_no")
        except:
            pass

    if 0 in [len(df_rt), len(df_sd)]:
        df = pd.concat([df_sd, df_rt])
        coll[id] = df
        continue
    if not len(df_rt.columns)==len(df_sd.columns):
        print("Different nunber of colummns.")
        print(df_rt.columns)
        print(df_sd.columns)
        coll[id] = df
        continue

    if np.all(df_rt.columns == df_sd.columns):
        pass
    else:
        print("Different colummns names, but numbers are equal.")
        print(df_rt.columns)
        print(df_sd.columns)

    df = pd.concat([df_sd, df_rt])
    dupl = df.index.duplicated(keep='first')
    print("n duplicates: %d" % len(np.where(dupl)[0]) )
    df = df[~dupl]

    coll[id] = df


for key in coll.keys():
    print(key)
    if len(coll[key])==0:
        print("No data")
        continue
    coll[key].insert(loc=1, column="datetime", value=coll[key].index)
    fpath = os.path.join(trgdir, "%d/%d_CRNS_merge.txt" % (key, key) )
    coll[key].to_csv(fpath, sep="\t", index=False, date_format="%Y-%m-%d %H:%M:%S")
