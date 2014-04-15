#!/bin/bash


count=0

<<<<<<< HEAD
#mkdir -p principal 
=======
mkdir -p fixture/principal 
>>>>>>> bafbefa0a53bfdee823041dbf6a5ac328de01053

for file in $( ls -1p fixture/*wrs.json )
do
    grep '"is_principal": true' ${file}
    if [[ $? -eq 0 ]]; then
	printf ">>> Move %s\n" ${file}
<<<<<<< HEAD
	mv ${file} fixture/todo/
=======
	mv ${file} fixture/principal
>>>>>>> bafbefa0a53bfdee823041dbf6a5ac328de01053
	count=$((count + 1))
    fi
done

printf '... %d\n' ${count}
