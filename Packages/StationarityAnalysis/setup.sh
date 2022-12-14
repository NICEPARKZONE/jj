#!/bin/bash 

# SonarAnalysis/Stationarity Analysis Package Setup Script
#
# Author: pedrohblisboa@gmail.com
#

# Check Env Variables



if [ -z "$SONAR_WORKSPACE" ]; then
	echo 
    echo "DO main setup.sh"
    echo
    return
fi  


source $SONAR_WORKSPACE/setup.sh

export MY_PATH=$PWD

export PACKAGE_NAME=$OUTPUTDATAPATH/StationarityAnalysis

# Folder Configuration
if [ -d "$OUTPUTDATAPATH/StationarityAnalysis" ]; then
    read -e -p "Folder $OUTPUTDATAPATH/StationarityAnalysis exist, Do you want to erase it? [Y,n] " yn_erase
    if [ "$yn_erase" = "Y" ]; then
    	echo
        echo "creating OUTPUTDATAPATH struct"
        echo
        rm -rf $PACKAGE_NAME
        mkdir $PACKAGE_NAME
        cd $SONAR_WORKSPACE/Packages/Classification
        for i in $(ls -d */); do 
    		mkdir $PACKAGE_NAME/${i%%/};
    		mkdir $PACKAGE_NAME/${i%%/}/pictures_files;
    		mkdir $PACKAGE_NAME/${i%%/}/output_files;
            # mkdir $PACKAGE_NAME/${i%%/}/classifiers_files;
            # mkdir $PACKAGE_NAME/${i%%/}/train_info_files;
    	done
        cd $MY_PATH
    else
    	echo
    	echo "Only Export Env Variables"
    	echo 
    fi

else
	echo
    echo "OUTPUTDATAPATH: $OUTPUTDATAPATH doesnt exists"
    echo "creating OUTPUTDATAPATH/StationarityAnalysis struct"
    echo
    rm -rf $PACKAGE_NAME
    mkdir $PACKAGE_NAME
    cd $SONAR_WORKSPACE/Packages/Classification
    for i in $(ls -d */); do 
    	mkdir $PACKAGE_NAME/${i%%/};
    	mkdir $PACKAGE_NAME/${i%%/}/pictures_files;
    	mkdir $PACKAGE_NAME/${i%%/}/output_files;
        # mkdir $PACKAGE_NAME/${i%%/}/classifiers_files;
        # mkdir $PACKAGE_NAME/${i%%/}/train_info_files;
    done
fi

