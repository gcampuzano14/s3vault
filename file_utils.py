import os
import shutil
import hashlib
import json


def calc_file_hash(file_name):
    # Open,close, read file and calculate MD5 on its contents 
    with open(file_name, 'rb') as file_to_check:
        # read contents of the file
        data = file_to_check.read() 
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
        return md5_returned


def move_media():
    crossed_media = []
    testpath = os.path.join(os.getcwd(), 'test')
    dirs = os.listdir(testpath)

    if '.DS_Store' in dirs:
        poper = dirs.index('.DS_Store')
        dirs.pop(poper)

    yrmos = {}

    for dr in dirs:
        yrmo = dr[0:6]
        if yrmo not in yrmos:
            yrmos[yrmo] = [{
                    'origin_src': dr,
                    'media': os.listdir(
                                    os.path.join(
                                        os.getcwd(),
                                        'test',
                                        dr))
                        }]
        else:
            moremedia = {
                    'origin_src': dr,
                    'media': os.listdir(os.path.join(
                                        os.getcwd(),
                                        'test',
                                        dr))}
            yrmos[yrmo].append(moremedia)

    print(yrmos)

    for key in yrmos:
        src = os.path.join(os.getcwd(), 'test')
        dest = os.path.join(os.getcwd(), 'dest', key)
        print(key)
        if key not in os.listdir(os.path.join(os.getcwd(), 'dest')):
            os.mkdir(dest)

        for element in yrmos[key]:
            if len(element['media']) > 0:
                print(element)
                print(element['origin_src'])
                for mediafile in element['media']:
                    fsrc = os.path.join(src, element['origin_src'], mediafile)
                    shutil.copy2(fsrc,
                                 os.path.join(dest, mediafile))
                    line = {'src': fsrc,
                            'dest': os.path.join(dest, mediafile)}
                    crossed_media.append(line)
    return crossed_media


def verify_integrity(crossed_media):

    failed = []

    for line in crossed_media:
        md5_returned = calc_file_hash(line['dest'])
        original_md5 = calc_file_hash(line['src'])

        if original_md5 == md5_returned:
            print "MD5 verified."
            pass
        else:
            print "MD5 verification failed!."
            failed.append(line['src'])
    print(failed)

if __name__ == '__main__':

    # crossed_media = move_media()
    # with open('crossed_media.json', 'w') as cm:
    #     cm.write(json.dumps(crossed_media))

    with open('crossed_media.json', 'r') as cm:
        crossed_media = json.loads(cm.read())

    verify_integrity(crossed_media)
