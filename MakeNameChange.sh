#!/bin/sh

if [ $# != 3 ]; then
    echo "参数不足，格式：./MakeNameChange ProjectPath OldPrefix NewProfix"
    exit 1
fi

if [ ! -d $1 ]; then
    echo "项目文件夹 $1 不存在，请检查"
    exit 1 
fi

if [ $3 = "YMU" ]; then
    echo "$3 这个前缀由于历史原因不能用，还是换一个吧"
    exit 1
fi

ProjectPath=$1
OldPrefix=$2
NewPrefix=$3
filterExtern=".*"
litterOldPrefix=`echo $OldPrefix | tr 'A-Z' 'a-z'`
litterNewPrefix=`echo $NewPrefix | tr 'A-Z' 'a-z'`
longReplace="s/${litterOldPrefix}_/${litterNewPrefix}_/g; s/${litterOldPrefix}th_/${litterNewPrefix}th_/g; s/${litterOldPrefix}fx_/${litterNewPrefix}fx_/g; s/k${OldPrefix}/k${NewPrefix}/g"

# 不需要修改的文件名和类名，这些改了后会比较麻烦，所以保留
UnChangeFile=("OWSFXConfiguration" "OWSFXSDKManager" "OWSFXManagerHeader" "UWPFXBusiness" "UWPFXDataInfo")
UnChangeCls=("OWSFXConfiguration" "OWSFXUser" "OWSFXReportItem" "OWSFXBusinessItem" "OWSFXBusinessCallBack" "OWSFXSDKManager")

echo "即将修改项目文件夹 ${ProjectPath} 现在的前缀 ${OldPrefix} 为 ${NewPrefix} "

TotalFiles=`find $ProjectPath -name "${OldPrefix}*${filterExtern}" | wc -l`
echo "共有前缀为 ${OldPrefix} 的文件 ${TotalFiles} 个。"

Files=`find $ProjectPath -type f -name "${OldPrefix}*${filterExtern}"`
XcodeProjs=`find $ProjectPath -name "*.xcodeproj"`

echo "开始处理以${OldPrefix}开头的文件"
for file in $Files; do
    
    filePath=${file%/*}
    fileName=${file##*/}
    externName=${file##*.}
    newFileName=${fileName/${OldPrefix}/${NewPrefix}}
    shortName=${fileName%.*}
    newTargetFile=${filePath}/${newFileName}
    thisFileWillBeChanged=true

    # 修改方法前缀
    echo "  ├修改文件 ${fileName} 中的 ${litterOldPrefix}_ 为 ${litterNewPrefix}_"
    sed -i .bk "${longReplace}" ${file}
    rm -rf ${file}.bk

    for unChange in ${UnChangeFile[@]}; do
        if [ "$shortName" = "$unChange" ]; then
            thisFileWillBeChanged=false
            break
        fi
    done

    if [ $thisFileWillBeChanged = false ]; then
        continue
    fi

    echo "  ├处理文件: ${file}"
    
    # 修改文件内容
    if [ $externName = "h" ]; then
        echo "    ├修改头文件 ${fileName} , 需要修改引用了这个头文件的想关文件..."
        for ContentFile in `find $ProjectPath -type f \( -name "${OldPrefix}*${filterExtern}" -o -name "${NewPrefix}*${filterExtern}" \) -exec grep ${fileName} {} -l \;`; do
            echo "      ├相关文件 ${ContentFile} "
            sed -i .bk "s/${shortName}\.h/${newFileName}/g" ${ContentFile}
            rm -rf ${ContentFile}.bk
        done
    else
        echo "    ├修改文件 ${fileName} 的内容..."
        sed -i .bk "s/${shortName}\.${externName}}/${newFileName}/g" ${file}
        rm -rf ${file}.bk
    fi
    # 文件改名
    echo "  ├改文件名 ${file} 为 ${newTargetFile}"
    mv "$file" "${newTargetFile}"

    # 修改 project.pbxproj 文件，使改名后的文件引入到项目里，同时移除旧文件名
    for projectDir in $XcodeProjs; do
        echo "    ├修改项目配置文件 ${projectDir}/project.pbxproj"
        sed -i .bk "s/${shortName}\.${externName}/${newFileName}/g" ${projectDir}/project.pbxproj
        rm -rf ${ProjectPath}/project.pbxproj.bk
    done
done
echo ""

echo "修改类名:"
# 找出所有的类名
Classes=`find $ProjectPath -name "${NewPrefix}*${filterExtern}" -exec grep -Pio "(?<=@interface )${OldPrefix}(.*?)(?= :)" {} \;`
# 修改类名
for clsName in $Classes; do
    willBeChanged=true

    for cls in ${UnChangeCls[@]}; do
        if [ "$clsName" = "$cls" ]; then
            willBeChanged=false
            break
        fi
    done
    
    if [ $willBeChanged = false ]; then
        continue
    fi

    newClsName=${clsName/${OldPrefix}/${NewPrefix}}
    echo "  ├修改类名: ${clsName} ==> ${newClsName}"
    
    # 替换类名 
    for ContainFile in `find $ProjectPath -type f \( -name "${NewPrefix}*${filterExtern}" -o -name "${OldPrefix}*${filterExtern}" \) -exec grep "${clsName}" {} -l \;`; do
        echo "    ├修改文件 ${ContainFile} 中的 ${clsName} 为 ${newClsName}"
        sed -i .bk "s/${clsName}/${newClsName}/g" ${ContainFile}
        # 修改方法前缀
        echo "    ├修改文件 ${fileName} 中的前缀含 ${OldPrefix} 的部分"
        sed -i .bk "s/${litterOldPrefix}_/${litterNewPrefix}_/g; s/k${OldPrefix}/k${NewPrefix}/g" ${ContainFile}

        rm -rf ${ContainFile}.bk
    done
done
echo ""

echo "几个特殊文件处理:"
find $ProjectPath -name "YMUSDKitCOF-Prefix.pch" -exec sed -i .bk "s/${OldPrefix}/${NewPrefix}/g" {} \;
find $ProjectPath -name "client.mm" -exec sed -i .bk "s/${OldPrefix}APICode\.h/${NewPrefix}APICode.h/g" {} \;
find $ProjectPath -name "UIImage+${OldPrefix}Base64.m" -exec sed -i .bk "s/${OldPrefix}DataToolKit\.h/${NewPrefix}DataToolKit.h/g" {} \;
find $ProjectPath -name "UIImage+${OldPrefix}Base64.m.bk" -exec rm -rf {} \;

find $ProjectPath -type f \( -name "client.*" -o -name "encoding.*" -o -name "${litterOldPrefix}_md5.*" -o -name "log.*" -o -name "xxtea.*" -o -name "UIImage+${OldPrefix}Base64.*" \) -exec sed -i .bk "${longReplace}" {} \;
find $ProjectPath -type f \( -name "YMUSDKitCOF-Prefix.pch.bk" -o -name "encoding.*.bk" -o -name "${litterOldPrefix}_md5.*.bk" -o -name "client.*.bk" -o -name "log.*.bk" -o -name "xxtea.*.bk" -o -name "UIImage+${OldPrefix}Base64.*.bk" \) -exec rm -rf {} \;

for file in `find $ProjectPath -type f -name "${litterOldPrefix}_md5.*"`; do
    filePath=${file%/*}
    fileName=${file##*/}
    externName=${file##*.}
    newFileName=${fileName/${litterOldPrefix}/${litterNewPrefix}}
    shortName=${fileName%.*}
    newTargetFile=${filePath}/${newFileName}

    mv $file $newTargetFile
    for projectDir in $XcodeProjs; do
        echo "    ├修改项目配置文件 ${projectDir}/project.pbxproj"
        sed -i .bk "s/${shortName}\.${externName}/${newFileName}/g" ${projectDir}/project.pbxproj
        rm -rf ${ProjectPath}/project.pbxproj.bk
    done
done

echo "Category 文件的处理"
CategoryFiles=`find $ProjectPath -type f -name "*+${OldPrefix}*${filterExtern}"`
for file in $CategoryFiles; do
    echo "  ├处理文件: ${file}"
    filePath=${file%/*}
    fileName=${file##*/}
    externName=${file##*.}
    newFileName=${fileName/${OldPrefix}/${NewPrefix}}
    shortName=${fileName%.*}
    newShortName=${shortName/${OldPrefix}/${NewPrefix}}
    newTargetFile=${filePath}/${newFileName}
    categoryName=${shortName##*+}
    newCategoryName=${categoryName/${OldPrefix}/${NewPrefix}}

    echo "    ├修改文件 ${fileName} , 修改Category名称为 (${newCategoryName})"
    sed -i .bk "s/(${categoryName})/(${newCategoryName})/g; s/${shortName}\.${externName}/${newFileName}/g; ${longReplace}" ${file}
    
    # 修改文件内容
    if [ $externName = "h" ]; then
        echo "    ├修改头文件 ${fileName} , 需要修改引用了这个头文件的想关文件..."
        for ContentFile in `find $ProjectPath -type f \( -name "${OldPrefix}*${filterExtern}" -o -name "${NewPrefix}*${filterExtern}" \) -exec grep ${fileName} {} -l \;`; do
            echo "      ├相关文件 ${ContentFile} "
            sed -i .bk "s/${shortName}\.h/${newFileName}/g" ${ContentFile}
            rm -rf ${ContentFile}.bk
        done
    else 
        sed -i .bk "s/${shortName}\.h/${newShortName}.h/g" ${file}
    fi
    rm -rf ${file}.bk
    # 文件改名
    echo "  ├改文件名 ${file} 为 ${newTargetFile}"
    mv "$file" "${newTargetFile}"

    # 修改 project.pbxproj 文件，使改名后的文件引入到项目里，同时移除旧文件名
    for projectDir in $XcodeProjs; do
        echo "    ├修改项目配置文件 ${projectDir}/project.pbxproj"
        sed -i .bk "s/${shortName}\.${externName}/${newFileName}/g" ${projectDir}/project.pbxproj
        rm -rf ${ProjectPath}/project.pbxproj.bk
    done
done

echo "处理Block"
for block in `find $ProjectPath -type f -name "${NewPrefix}*.*" -exec grep -Pio "(?<=\(\^)${OldPrefix}.*?(?=\))" {} \;`; do
    newBlockName=${block/${OldPrefix}/${NewPrefix}}
    echo "  ├修改Block ${block} 为 ${newBlockName}"
    for file in `find $ProjectPath -type f \( -name "${NewPrefix}*.*" -o -name "${OldPrefix}*.*" \) -exec grep $block {} -l \;`; do
        sed -i .bk "s/${block}/${newBlockName}/g" $file
        rm -rf ${file}.bk
    done
done

echo "处理文件夹名字: 现脚本只能处理 2 层的文件夹，第三层的话还要继续改脚本"
list=`find $ProjectPath -type d \( -name "${OldPrefix}*" ! -name "*(deprecated)" \) | awk '{ print length, $0 }' | sort -n -s | awk '{ print $2 }'`
for item in ${list[@]}; do
    OldDirName=${item##*/}
    NewDirName=${OldDirName/${OldPrefix}/${NewPrefix}}
    NewName=${item//${OldPrefix}/${NewPrefix}}
    count=`echo $item | grep -o ${OldPrefix} | wc -l`
    if [ $count = 1 ]; then
        echo "修改文件夹 ${item} 为 ${NewName}"
        mv -n $item $NewName
    else
        NewDir=${item/${OldPrefix}/${NewPrefix}}
        echo "修改文件夹 ${NewDir} 为 ${NewName}"
        mv -n $NewDir $NewName
    fi

    # 修改 project.pbxproj 文件
    for projectDir in $XcodeProjs; do
        echo "    ├修改项目配置文件 ${projectDir}/project.pbxproj"
        sed -i .bk "s/${OldDirName}/${NewDirName}/g" ${projectDir}/project.pbxproj
        rm -rf ${ProjectPath}/project.pbxproj.bk
    done
done

# echo "处理enum"
# for type in `find $ProjectPath -type f -name "${NewPrefix}*.*" -exec grep -Pio "(?<=typedef NS_ENUM\(NSUInteger, )(.*?)(?=\))|(?<=typedef NS_ENUM\(NSInteger, )(.*?)(?=\))" {} \;`; do
#     # 这个 OWSFormatCode 接入端也会用到，一直改的会接入端也要跟着改
#     if [ $type = "OWSFormatCode" ]; then
#         continue
#     fi

#     newType=${type/${OldPrefix}/${NewPrefix}}
#     if [ $type = $newType ]; then 
#         continue
#     fi
#     echo "  ├修改类型 ${type} 为 ${newType}"
#     for file in `find $ProjectPath -type f -name "${NewPrefix}*.*" -exec grep -Pio "${type}" -l {} \;`; do
#         sed -i .bk "s/${type}/${newType}/g" ${file}
#         rm -rf ${file}.bk
#     done
# done

# Methods=`grep -h -r -I "^[-+]" "./" --include '*.[mh]' | sed "s/[-+]//g" | sed "s/[();,:*\^\/\{]/ /g" | sed "s/[ ]*</</" | sed "/^[ ]*IBAction/d" | awk '{split($0,b," "); print b[2];}' | sort | uniq | sed "/^$/d" | sed -n "/^${litterOldPrefix}_/p"`
# for method in $Methods; do
#     echo "修改方法 ${method} "
#     newMethod=${method/${litterOldPrefix}/${litterNewPrefix}}
#     for file in `find /work/iosfxsdkcopy -type f -name "OBS*.*" -exec grep "${method}" -l {} \;`; do
        
#     done
# done

echo "处理完成"
