#!/bin/bash


count=0

#mkdir -p principal 

for file in $( ls -1p fixture/*wrs.json )
do
    grep '"is_principal": true' ${file}
    if [[ $? -eq 0 ]]; then
	printf ">>> Move %s\n" ${file}
	mv ${file} fixture/todo
	count=$((count + 1))
    fi
done

printf '... %d\n' ${count}
