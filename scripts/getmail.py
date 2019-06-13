
# coding: utf-8

# In[13]:


import imaplib
import email
import numpy as np
import pandas as pd
import os
import sys
import datetime as dt

geckopicspass = sys.argv[1]
trgroot = sys.argv[2]

# In[15]:


# CONFIG

# ID
crns = [16, 17, 18, 19, 23, 24]

# First line in dataset
headerline = ["//Hydroinnova CRS-1000 Data",
               "//Hydroinnova CRS-1000 Data",
               "//Hydroinnova CRS-1000 Data",
               "//CRS-DL2100 Data",
               "//Hydroinnova CRS-1000 Data",
               "//Hydroinnova CRS-1000 Data"]

# Column names for the different crns
colnames = [
    ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"],
    ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"],
    ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"],
    ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "temp_ext", "relhum_ext"],
    ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"],
    ["rec_id", "datetime", "press1", "temp1", "relhum1", "volt", "counts1", "nsecs1", "counts2", "nsecs2", "temp_ext", "relhum_ext"]
]

# Target directory
#trgroot = "/media/x/cosmicsense/b2drop_copy/cosmicsense/inbox/fendt/timeseries/crns/JFC-1"
tmpfile = "tmpfile"


# In[16]:


mail = imaplib.IMAP4_SSL('imap.uni-potsdam.de')
mail.login('geckopics', geckopicspass)
mail.list()
mail.select('inbox')


# In[17]:


for i, crn in enumerate(crns):
    print("CRNS with ID:", crn)
    numcommas = len(colnames[i])-1
    # reset tmpfile
    if os.path.exists(tmpfile):
        os.remove(tmpfile)
    # all mails with data for that crns
    if crn==19:
        subject = '%03d Data' % crn
    else:
        subject = '%03d_Data' % crn
    result, data = mail.uid('search', None, '(SUBJECT "%s")' % subject)
    for uid in data[0].split():
        latest_email_uid = uid
        print("\t", latest_email_uid)
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
        # fetch the email body (RFC822) for the given ID
        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        # converts byte literal to string removing b''
        email_message = email.message_from_string(raw_email_string)
        for part in email_message.walk():
            if part.get_content_type() == "text/plain": # ignore attachments/html
                body = part.get_payload(decode=True)
                body = body.decode('utf-8')
                lines = body.split("\n")
                for line in lines:
                    # comment line?
                    if "//" in line:
                        continue
                    # empty line?
                    if line=="":
                        continue
                    # correct number of records?
                    line = line.strip()
                    line = line.strip(",")
                    if not line.count(",")==numcommas:
                        continue
                    # does datetime parse correctly?
                    dtimestr = line.split(",")[1].strip()
                    try:
                        dtime = dt.datetime.strptime(dtimestr, "%Y/%m/%d %H:%M:%S")
                    except ValueError:
                        print("Corrupt datetime")
                        continue
                    line = line+"\n"
                    myfile = open(tmpfile, 'a')
                    myfile.write(line)
                    # body is again a byte literal
                    myfile.close()
            else:
                continue
    df = pd.read_csv(tmpfile, sep=",", header=None,
                     error_bad_lines=False, warn_bad_lines=True, na_values=[-99.0])
    df.columns = colnames[i]
    # Eliminate corrupt rows which are incomplete
    df = df.drop(np.where(df.counts1.isna())[0])
    df.datetime = pd.to_datetime(df.datetime, format="%Y/%m/%d %H:%M:%S")
    fpath = os.path.join(trgroot, "%d/%d_CRNS.txt" % (crn, crn))
    df.to_csv(fpath, sep="\t", index=False, date_format="%Y-%m-%d %H:%M:%S")
    os.remove(tmpfile)
