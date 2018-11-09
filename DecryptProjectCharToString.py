#!/usr/bin/python3
#-*- coding: utf-8 -*-

import importlib
import os
import re
import sys
import base64

def matchCharToString(match):
    needReplaceStr = match.group(2)
    decryptStr = ""
    for ch in list(needReplaceStr.split(',')):
        if int(ch) != 0:
            decryptStr = decryptStr + "%c" % int(ch)
    # replacedStr = '\"' + decryptStr + '\"'
    base64DecodeStr = base64.b64decode(decryptStr.encode()).decode()
    replacedStr = '\"' + base64DecodeStr + '\"'
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

def decryptFile(filePath, reg):
    sourceCode = readSourceCode(filePath)
    sourceCode = re.sub(reg, matchCharToString, sourceCode)
    return sourceCode

def decrypt(projectPath):
    for parent, dirnames, filenames in os.walk(projectPath):
        for filename in filenames:
            filePath = os.path.join(parent, filename)
            extendedName = os.path.splitext(filePath)
            if (extendedName[1] == '.h' or extendedName[1] == '.m' or extendedName[1] == '.mm'):
                print("解密文件: " + filePath)
                decryptedCode = decryptFile(filePath, r'(UWPStr\(|confusion_CSTRING\()\(\(char \[\]\) \{(.*?)\}\)(\))')
                decryptedCode = re.sub(r'[/]*#define UWPEncryptedString', '//#define UWPEncryptedString', decryptedCode)
                saveSourceCode(decryptedCode, filePath)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("请输入项目路径。")
        sys.exit()
    projectPath = sys.argv[1]
    if len(projectPath) > 0:
        decrypt(projectPath)
    else:
        print("路径有误，请重新输入。")
        sys.exit()

