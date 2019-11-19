#!/usr/bin/env python
import requests
import argparse

__author__ = 'mustafauzun0'

'''
FINDZIP
'''

def main():
    parser = argparse.ArgumentParser(description='Find Zip Files in Website')
    
    parser.add_argument('-u', '--url', dest='url', type=str, help='Website URL', required=True)
    parser.add_argument('-f', '--file', dest='file', type=str, help='Wordlist File', required=True)
    parser.add_argument('-o', '--output', dest='output', help='Output File Finding Zip Files')


    args = parser.parse_args()

    zipFileExtensions = [ 'zip', 'rar', 'taz', 'tar', 'tar.z', 'tar.gz', 'gzip', 'gzi', 'gz', 'bz', 'bz2', 'bzip', 'bzip2', '7z', '7z.001', '7z.002' ]
    zipFileContentType = [ 'application/zip', 'application/x-rar-compressed', 'application/x-gzip', 'application/x-bzip', 'application/x-7z-compressed' ]
    findFiles = []

    if args.file:  
        with open(args.file, 'r') as file:
            wordlist = file.readlines()

            for word in wordlist:
                for extension in zipFileExtensions:
                    checkURL = 'http://{url}/{fileName}.{extension}'.format(url=args.url.rstrip('/'), fileName=word.strip(), extension=extension)

                    try:
                        request = requests.get(checkURL, allow_redirects=False)

                        if request and request.headers['content-type'] in zipFileContentType:
                            if checkURL not in findFiles:
                                findFiles.append(checkURL)
                    except:
                        pass
    
    if args.output:
        try:
            file = open(args.output, 'w')
            file.write('\n'.join(findFiles))
            file.close()
        except IOError:
            print('[-] Unable to create file on disk')
    else:
        if findFiles:
            print(*findFiles, sep='\n')
    
    
if __name__ == '__main__':
	main()