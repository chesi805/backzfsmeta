#! /usr/bin/python
import commands
import os
import sys
import logging

poolnames = []
def backup_label(flag,pool_name):
    ret, output = commands.getstatusoutput("/usr/sbin/zpool status %s" % pool_name)
    if ret != 0:
        logging.warning("get pool %s status fail." % pool_name)
	return 0, pool_name
        
    lines = output.split("\n")

    for line in lines:
        if "JBOD" in line:
            line2 = line.split()[0]
            ret, output = commands.getstatusoutput("dd if=/dev/mapper/%s bs=256k count=1 of=/root/%s_%s_label_%d" % (line2, pool_name, line2.split("_")[-1],flag))
            #name="/root/%s_%s_label%d"%(pool_name, line2.split("_")[-1],flag)
            #logging.debug(name)
        elif "dm" in line:
            line2 = line.split()[0]
            ret, output = commands.getstatusoutput("dd if=/dev/%s bs=256k count=1 of=/root/%s_%s_label_%d" % (line2, pool_name, line2,flag))
        else:
            continue

def get_poolname():
    ret, output = commands.getstatusoutput("/usr/sbin/zpool list")
    if ret != 0:
        logging.warning("listpool fail.")
        return 0

    lines = output.split("\n")
    
    for line in lines:
        if "PoolID" in line or "NAME" in line:
            continue
        else:
            poolnames.append(line.split()[0])

    return poolnames

def handle_save_meta(flag):
    poolnames = get_poolname()
    logging.debug(poolnames)
    if poolnames == 0:
        logging.warning("call the get_poolname() fail.")
    else:
        for pool in poolnames:
            logging.debug(pool)
            backup_label(flag,pool)
    
