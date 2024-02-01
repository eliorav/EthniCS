import argparse
from pathlib import Path
import shutil
import pandas as pd
from tqdm import tqdm
import argparse
import json
import os
import shutil
import urllib.request as request
from contextlib import closing
from config import DOWNLOAD_FOLDER, LIST_PATH, FTP_PROXY, DATA_FTP_SERVER

def load_json(path):
    """
    Load a JSON file from the given path and return its contents as a dictionary.

    Args:
        path (str): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    with open(path) as f:
        return json.load(f)

READINTO_BUFSIZE = 1024 * 1024

def _copyfileobj_readinto(fsrc, fdst, callback, length=0):
    """
    Read data from the source file object and write it to the destination file object using the readinto() method.

    Args:
        fsrc (file object): The source file object.
        fdst (file object): The destination file object.
        callback (function): A callback function to track the progress of the file copy.
        length (int, optional): The number of bytes to read from the source file at a time. Defaults to 0.

    Returns:
        None
    """
    fsrc_readinto = fsrc.readinto
    fdst_write = fdst.write

    if not length:
        try:
            file_size = os.stat(fsrc.fileno()).st_size
        except OSError:
            file_size = READINTO_BUFSIZE
        length = min(file_size, READINTO_BUFSIZE)

    copied = 0
    with memoryview(bytearray(length)) as mv:
        while True:
            n = fsrc_readinto(mv)
            if not n:
                break
            elif n < length:
                with mv[:n] as smv:
                    fdst.write(smv)
            else:
                fdst_write(mv)
            copied += n
            callback(copied)

def copyfileobj(fsrc, fdst, callback, length=0):
    """
    Copy the contents of the source file object to the destination file object.

    Args:
        fsrc (file object): The source file object.
        fdst (file object): The destination file object.
        callback (function): A callback function to track the progress of the file copy.
        length (int, optional): The number of bytes to read from the source file at a time. Defaults to 0.

    Returns:
        None
    """
    try:
        # check for optimisation opportunity
        if "b" in fsrc.mode and "b" in fdst.mode and fsrc.readinto:
            return _copyfileobj_readinto(fsrc, fdst, callback, length)
    except AttributeError:
        # one or both file objects do not support a .mode or .readinto attribute
        pass

    if not length:
        length = shutil.COPY_BUFSIZE

    fsrc_read = fsrc.read
    fdst_write = fdst.write

    copied = 0
    while True:
        buf = fsrc_read(length)
        if not buf:
            break
        fdst_write(buf)
        copied += len(buf)
        callback(copied/1024/1024/1024)

def download_sample_ftp(args):
    """
    Download sample files from FTP server based on the provided arguments.

    Args:
        args (argparse.Namespace): The command-line arguments.

    Returns:
        None
    """
    try:
        df = pd.read_csv(LIST_PATH)
        
        sample_info = df.iloc[args.sample_idx-1]
        download_folder = Path(args.output_folder)/DOWNLOAD_FOLDER
        print(f"downloading {sample_info['name']}")

        out_folder = download_folder/sample_info['ethnicity']/sample_info['name']
        out_folder.mkdir(exist_ok=True, parents=True)   

        for ftp_path in [sample_info['bai'], sample_info['bam']]:
            req = request.Request(f'{DATA_FTP_SERVER}/{ftp_path}')
            req.set_proxy(args.ftp_proxy, 'http')

            with closing(request.urlopen(req)) as r:
                with tqdm(total=r.length) as pbar:
                    with open(out_folder/Path(ftp_path).name, 'wb') as f:
                        copyfileobj(r, f, pbar.update)

    except Exception as e:
        print(e)


def main(args):
    """
    Main function to download sample files from FTP server.

    Args:
        args (argparse.Namespace): The command-line arguments.

    Returns:
        None
    """
    download_sample_ftp(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="merge the samples into pool.")
    parser.add_argument(
        "--output_folder",
        help="The output folder",
    )
    parser.add_argument(
        "--sample_idx",
        type=int,
        help="The number of the current pool",
    )
    parser.add_argument('--ftp_proxy', default=FTP_PROXY, type=str)
    args = parser.parse_args()

    if args.ftp_proxy is not None:
        os.environ["ftp_proxy"] = args.ftp_proxy

    main(args)