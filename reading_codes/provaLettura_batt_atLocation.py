#BOZZA CODICE PER LETTURA LIVELLO BATTARIA DA LOG_FILE CON VALORE DI RITORNO BOOLEANO: TRUE SE LIVELLO BATTERIA MAGGIORE DI 30 FALSE SE MINORE

import re
import numpy as np
import json

# input file name with extension
# entering try block
try:
	file_name = 'log.txt'
	file_read = open(file_name, "r")
	text = 'Reply'
	lines = file_read.readlines()

# controlla se la riga contiene "reply" e nel caso la aggiunge alla lista 	

	rep_list = []
	idx = 0
	
	for line in lines:
		if text in line:
			rep_list.insert(idx, line)
			idx += 1
	file_read.close()
	if len(rep_list)==0:
		print("\n\"" +text+ "\" is not found in \"" +file_name+ "\"!")
	else:
		print("\n** Battery level check: **")
		#print(rep_list)

	float_list = []
	ind = 0
	lineLen = len(rep_list)
	for i in range(lineLen):
 		float_values = [float(s) for s in re.findall(r'-?\d+\.?\d*', rep_list[i])]
 		float_list.insert(ind, float_values)
 		#print(float_list)
	val1= [0.0]
	val2= [1.0]
	val3= [2.0]
	val4= [3.0]
	val5= [1.0, 32.0, 0.0]
	bat_liv_list = list(filter(None, float_list))
	bat_liv_list = list(filter((val1).__ne__, bat_liv_list))
	bat_liv_list = list(filter((val2).__ne__, bat_liv_list))
	bat_liv_list = list(filter((val3).__ne__, bat_liv_list))
	bat_liv_list = list(filter((val4).__ne__, bat_liv_list))
	bat_liv_list = list(filter((val5).__ne__, bat_liv_list))
	#print(bat_liv_list)
	
# converto la lista in un array di booleani per poter controllare se il valore è sotto la soglia 

	y = np.array(bat_liv_list)
	floatArray = y.astype(float)
	#print (floatArray) 
	floatArray = list(reversed(floatArray)) 

	print("** Check Battery Threshold: ** ""\n")

# registro la lista relativa al messaggio di isAtLocation

	isAtLocation = []
	idk = 0

	text1 = "isAtLocation"
	with open(file_name) as file_iterator:
		for line in file_iterator:
			if text1 in line:
				nex = next(file_iterator)
				nex_1 = next(file_iterator)
				#print(nex_1)
				isAtLocation.insert(idk, nex_1)
	#print(isAtLocation)

# estraggo gli interi dalla lista (0 e 1) 

	int_list = []
	ind_n1 = 0

	lineLen = len(isAtLocation)
	for i in range(lineLen):
  		int_values = [int(temp)for temp in isAtLocation[i].split() if temp.isdigit()]
  		int_list.insert(ind_n1, int_values)

	int_list = list(filter(None, int_list))
	y1 = np.array(int_list)

	#print("isAtLocation: \n")

	mid_bat_thre = 50.0
	min_bat_thre = 30.0
	BATTERY_30 = False
	BATTERY_50 = False
	location = False
	total_trace = []

# verifico il valore di batteria e della location e attribuisco valori booleani

	lineLen = len(int_list)
	for i in range(lineLen):
		if floatArray[i] > mid_bat_thre and y1[i] == 0:
 			BATTERY_30 = True
 			BATTERY_50 = True
 			location = False
 			TRACE = [BATTERY_30,BATTERY_50,location]
 			total_trace.append(TRACE)

		elif floatArray[i] > mid_bat_thre and y1[i] == 1:
 			BATTERY_30 = True
 			BATTERY_50 = True
 			location = True
 			TRACE = [BATTERY_30,BATTERY_50,location]
 			total_trace.append(TRACE)
		
		elif floatArray[i] > min_bat_thre and floatArray[i] < mid_bat_thre and y1[i] == 0: 
 			BATTERY_30 = True
 			BATTERY_50 = False
 			location = False
 			TRACE = [BATTERY_30,BATTERY_50,location]
 			total_trace.append(TRACE)

		elif floatArray[i] > min_bat_thre and floatArray[i] < mid_bat_thre and y1[i] == 1: 
 			BATTERY_30 = True
 			BATTERY_50 = False
 			location = True
 			TRACE = [BATTERY_30,BATTERY_50,location]
 			total_trace.append(TRACE)

		elif floatArray[i] < min_bat_thre and y1[i] == 0:
			BATTERY_30 = False
			BATTERY_50 = False
			location = False
			TRACE = [BATTERY_30,BATTERY_50,location]
			total_trace.append(TRACE)

		elif floatArray[i] < min_bat_thre and y1[i] == 1:
			BATTERY_30 = False
			BATTERY_50 = False
			location = True
			TRACE = [BATTERY_30,BATTERY_50,location]
			total_trace.append(TRACE)

	print("Trace composition: [ BATTERY_30, BATTERY_50, isAtLocation]")
	print('Json trace: \n')
	final = json.dumps(total_trace)
	print(final)

# # le due righe qui sotto producono un file json contenente la traccia

	with open("final.json", "w") as outfile:
 		json.dump(total_trace, outfile)

# entering except block
except :
	print("\nThe file doesn't exist!")