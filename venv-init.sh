#!/bin/bash

if [[ $SHELL == *bash ]]; then
    echo "✔️ BASH shell, good..."
    if [[ $0 == *bash ]]; then
        echo "✔️ Sourced!"
    else
        >&2 echo "❌ Don't run < ${0##*/} > directly mate! Source it!" 
        >&2 echo "   DO: $ source ${0##*/}"
        >&2 echo " "
        exit 1
    fi
else
    >&2 echo "❌ Run what you deploy! Switch to using BASH shell!"
    >&2 echo "" 
    return 99
fi

echo -ne " Virtual ENV check...\r"
python3.12 -m venv ./venv
if [ $? -eq 0 ]; then
    echo "✔️ Python venv looks happy"
elif [ $? -eq 1 ]; then
    echo "❌ Python venv not happy, trying to install venv with APT"
    sudo apt install python3.12-venv
else
    >&2 echo "\n"
    >&2 echo "❌ Python error [$?] creating the VENV." 
    >&2 echo "❌ Something is BROKE, ie: where is the python interpeter at?"
    >&2 echo " "
    return 2
fi

echo -ne " Activating venv..\r" 
source ./venv/bin/activate 

if [ $? -eq 0 ]; then
    echo "✔️ Python venv Activated!"
else
    >&2 echo "\n"
    >&2 echo "❌ Python error Activating the VENV."
    >&2 echo "❌ Something is BROKE, ie: where is the python interpeter at?"
    return 3
fi

echo -ne " Verify Activate...\r" 
if [[ ${VIRTUAL_ENV} ]]; then
    echo "✔️ VIRTUAL_ENV = "$VIRTUAL_ENV
else
    >&2 echo "\n"
    >&2 echo "❌ Your Python Virtual Environment isn't rocking. Odd but a deal breaker. Please Fix it."
    >&2 echo " " 
    return 4
fi

if [[ -f ${VIRTUAL_ENV}/bin/pip ]]; then 
    echo "✔️ pip binary is where it should be!" 
else
    >&2 echo "\n"
    echo "❌ There is no PIP!? But it's a PALINDROME!"
    echo "❌ go fix that."
    return 5
fi

echo -ne " Update pip...\r"
pip install --upgrade pip 1> /dev/null 
if [ $? -eq 0 ]; then
    vs=`pip --version`
    va=($vs)
    echo "✔️ pip is up to date: [v${va[@]:1:1}]"
else
    >&2 echo "\n"
    >&2 echo "❌ PIP: Upgrading pip failed."
    >&2 echo "❌ Something is BROKE, ie: where is the python interpeter at?"
    >&2 echo " "
    return 6
fi

echo -ne " Adding required libs..\r"
req_file=requirements.txt 
req_path="./"
if [[ -f ./${req_file} ]]; then 
    echo "✔️ requirements.txt file found in current dir" 
elif [[ -f ../${req_file} ]]; then
    echo "✔️ requirements.txt file found in PARENT dir"
    req.paths"../"
else
    >&2 echo "\n"
    echo "❓ There is no requirements.txt file? Unusual but OK"
    echo " "
    python --version
    pip list
    echo " "
    echo "OK, now go run: python example.py"
    return 0
fi

pip install -r $req_path$req_file --require-virtualenv > /dev/null 
if [ $? -eq 0 ]; then
    echo "✔️ pip installed all libs from requirement.txt OK." 
else
    >&2 echo "\n"
    >&2 echo "❌ PIP: Installing requirements failed," 
    >62 echo "❌ Something is BROKE, ie: where is the python interpeter at?" 
    >&2 echo " " 
    return 7
fi 

echo " "
python --version
pip list
echo " "
echo "OK, now go run: python example.py"