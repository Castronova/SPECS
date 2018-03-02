#!/usr/bin/env python3

import os
import shutil

####################################
# Author: Tony Castronova
# Email:  acastronova.cuahsi.org
# Date:   10.23.2017
# Org:    CUAHSI
# Desc:   Entrypoint for executing the summa model
####################################


basedir = '/tmp/summa'

# these paths come in as absolute.  Grab everything after the initial "\"
summa_masterpath = os.environ['MASTERPATH']
#summa_basepath = os.environ['LOCALBASEDIR'][1:]
#summa_outpath = os.environ['OUTDIR']


def prepare():
    print('Preparing execution environment')


    # copy summa to temp location
    #abspath = os.path.join(basedir, summa_basepath)
#    tmppath = os.path.join('/tmp', '_exec')
#    tmpout = os.path.join(tmppath, summa_outpath)
#    outpath = os.path.join(basedir, summa_outpath)
#    exepath = os.path.join(tmppath, summa_masterpath)
    fm = os.path.join(basedir, summa_masterpath)
    assert os.path.exists(fm), 'Could not find masterfile at %s' % summa_masterpath

    tmp_fm = os.path.join(basedir, summa_masterpath+'_tmp')

    print('PATH: %s' % basedir)
#    print('TMP PATH: %s' % tmppath)
#    print('TMP OUT: %s' % tmpout)
#    print('OUTPATH: %s' % outpath)
#    print('EXE PATH: %s' % exepath)
    print('FM PATH: %s' % fm)
    print('TMP_FM PATH: %s' % tmp_fm)

    print('Creating the tmp Filemanager')
    args = {}
    with open(tmp_fm, 'w') as w:
        with open(fm, 'r') as r:
            lines = r.readlines()
            for line in lines:
                l = line.replace('<BASEDIR>', basedir)
                w.write(l)

                # save masterpath args
                path, id = l.split('!')
                path = path.strip().replace("'", "")
                id = id.strip()
                args[id] = path

    # make sure all these paths exist
    if not os.path.exists(args['output_path']):
        os.makedirs(args['output_path'])


    for k, v in args.items():
        if k in ['fman_ver', 'output_prefix']:
            pass
        elif 'path' in k:
            assert os.path.exists(v), "Error in masterfile. Could not find " \
                                      "%s: %s" % (k, v)
        else:
            p = os.path.join(args['setting_path'], v)
            assert os.path.exists(p), "Error in masterfile. Could not find " \
                                      "%s: %s" % (k, v)

    print('SUMMA PREP COMPLETE')
    return tmp_fm


    # remove the tmp execution directory if it already exists
#    rm_tmp_dir(basedir+'_exec')
#    print(tmppath)
#    print(outpath)
#    os.makedirs(tmppath)
#    mk_output_dir(outpath)

#    print('Copying simulation files to execution directory')
#    os.system('cp -r %s/* %s' % (basedir, tmppath))

    # modify filepaths in place
#    os.system('find %s -type f | xargs sed -i "s|<BASEDIR>|%s|"' % (tmppath, tmppath))

#os.system('find %s -type f | xargs sed -i "s|<BASEDIR>|%s|"'
#               % (tmp_fm, basedir))

#    for p in [tmppath, outpath, exepath]:
#        if not os.path.exists(p):
#            print('PATH ERROR: %s' % p)
#    print('tmppath: ' + tmppath)
#    print('outpath: ' + outpath)
#    print('exepath: ' + exepath)

#    assert os.path.exists(tmppath), '%s does not exist' % tmppath
#    assert os.path.exists(outpath), '%s does not exist' % outpath
#    assert os.path.exists(exepath), '%s does not exist' % exepath



def rm_tmp_dir(tmp):
    # remove the temporary directory
    if os.path.exists(tmp):
        print('Cleaning execution environment')
        shutil.rmtree(tmp)


def mk_output_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)


#def run(path, tmpout, outpath):
def run(masterp):
    print('Running SUMMA simulation')
    os.system('/code/bin/summa.exe -m %s' % masterp)

#    # move the output files to the original dir
#    if not os.path.exists(outpath):
#        os.makedirs(outpath)
#    os.system('cp -r %s/* %s' % (tmpout, outpath))

def clean(masterp):
    os.remove(masterp)

# entry point steps
masterp = prepare()
run(masterp)
clean(masterp)


#execpath, outtmp, outpath = prepare()
#run(execpath, outtmp, outpath)
#rm_tmp_dir('/tmp/summa_exec')
