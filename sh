#!/bin/bash
cd ~/iOSProjects/AutoLearning
appVer=$(xcodebuild -showBuildSettings | grep -F 'CURRENT_PROJECT_VERSION')
appVer=$(cat $appVer | grep -e '[0-9]*')
echo $appVer
