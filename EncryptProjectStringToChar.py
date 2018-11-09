#!/usr/bin/python3
#-*- coding: utf-8 -*-

import importlib
import os
import re
import sys
import base64

def matchStringToChar(match):
    needReplaceStr = match.group(2)
    base64EncodeStr = base64.b64encode(needReplaceStr.encode()).decode()
    # replacedStr = '\"' + base64EncodeStr + '\"'

    needReplaceStr = base64EncodeStr + '\x00'
    # needReplaceStr = match.group(2) + '\x00'
    replacedStr = '((char []) {' + ', '.join(["%i" % (ord(ch) if ch != '\0' else 0) for ch in list(needReplaceStr)]) + '})'
    return match.group(1) + replacedStr + match.group(3)

def readSourceCode(filePath):
    with open(filePath, 'r') as f:
        sourceCode = f.read()
        f.close()
        return sourceCode

def saveSourceCode(sourceCode, filePath):
    with open(filePath, 'w') as f:
        f.write(sourceCode)
        f.close()

def encryptFile(filePath, reg):
    sourceCode = readSourceCode(filePath)
    sourceCode = re.sub(reg, matchStringToChar, sourceCode)
    return sourceCode

def encrypt(projectPath):
    for parent, dirs, filenames in os.walk(projectPath):
        for filename in filenames:
            filePath = os.path.join(parent, filename)
            extendedName = os.path.splitext(filePath)
            if (extendedName[1] == '.h' or extendedName[1] == '.m' or extendedName[1] == '.mm'):
                print("处理文件: " + filePath)
                encryptedCode = encryptFile(filePath, r'(UWPStr\()"(.*?)"(\))')
                encryptedCode = re.sub(r'[/]*#define UWPEncryptedString', '#define UWPEncryptedString', encryptedCode)
                saveSourceCode(encryptedCode, filePath)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("请输入项目路径。")
        sys.exit()
    projectPath = sys.argv[1]
    if len(projectPath) > 0:
        encrypt(projectPath)
    else:
        print("路径有误，请重新输入。")
        sys.exit()

    
