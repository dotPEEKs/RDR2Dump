# Coded By dotPEEK
# Thanks For Using :)

import os
import base64
import sys
from argparse import ArgumentParser

list_dir = os.listdir

class FILEFORMAT:
    """
    For Checking JPEG file format
    """
    RDR2_FILE_FORMAT_END_HEADER = b'\x00JEND'
    RDR2_FILE_FORMAT_START_HEADER = b'\x00\x00\x00\x04F\x00O\x00T\x00O\x00\x1e\x01R\x00A\x00F\x00 \x00-\x00'
    JPEG_VALID_START_FILE_HEADER = b'\xff\xd8\xff\xe0\x00\x10JFIF'
    JPEG_VALID_END_OF_FILE_HEADER = b'\xff\xd9'
def check_file_format(content: bytes) -> bool:
    return content.startswith(FILEFORMAT.RDR2_FILE_FORMAT_START_HEADER) and content.endswith(FILEFORMAT.RDR2_FILE_FORMAT_END_HEADER) and FILEFORMAT.JPEG_VALID_START_FILE_HEADER in content and FILEFORMAT.JPEG_VALID_END_OF_FILE_HEADER in content

def print_succes(*args):
    print("[+] ",*args)
def print_fail(*args):
    print("[-] ",*args)
def print_status(*args):
    print("[*] ",*args)
def find_jpeg_data(content: bytes) -> bytes:
    return content[content.index(FILEFORMAT.JPEG_VALID_START_FILE_HEADER):content.index(FILEFORMAT.JPEG_VALID_END_OF_FILE_HEADER) + len(FILEFORMAT.JPEG_VALID_END_OF_FILE_HEADER)]
def extract_jpegs(path: str,target_path: str):
    count = 0
    print(path,target_path)
    if not os.path.exists(path):
        print_fail("Uygun olmayan patika ya da patika klasör değil: %s" % (path))
        sys.exit(1)
    if not os.path.exists(target_path) or os.path.isfile(target_path):
        target_path = os.path.join(os.getcwd(),"RDR2_DUMP" + base64.b16encode(os.urandom(4)).decode())
        print_fail("Hedef Patika uygun değil Bu Yüzden Patika Şununla değiştirildi: %s" % (target_path))
        os.makedirs(target_path)
    for files in list_dir(path):
        fixed_path = os.path.join(path,files)
        if os.path.getsize(fixed_path) > 100000000 or os.path.getsize(fixed_path) <= 0:
            print_fail("Geçerli olmayan dosya büyüklüğü: %s" % (fixed_path))
        else:
            with open(fixed_path,"rb") as fd:
                content = fd.read()
                if check_file_format(content):
                    print_succes("Geçerli dosya: %s" % (fixed_path))
                    with open(os.path.join(target_path,"rdr2_dump_" + base64.b16encode(os.urandom(4)).decode() + ".jpg"),"wb") as outfd:
                        outfd.write(find_jpeg_data(content))
                    count += 1
    if count > 1:
        print_succes("Total Çıkartılan Dosyalar: %s" % (count))
        print_succes("Çıkartılan klasör: %s" % (target_path))
        print("Programı kullandığınız için teşekkürler :) ")
if __name__ == "__main__":
    parser = ArgumentParser(epilog="RDR2 PHOTO Dumper coded by dotPEEK")
    parser.add_argument("-s","--source-dir",required=True,help="RDR2 Oyununun patikası ya da dump edilecek klasör")
    parser.add_argument("-t","--target-dir",required=False,help="Çıkartılan resimlerin ayıklanacak olan hedef klasörü default: %s\\RDR2_DUMP%s"  % (os.getcwd(),"X"*8),default='')
    parser = parser.parse_args()
    extract_jpegs(parser.source_dir,parser.target_dir)