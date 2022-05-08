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
	print("\n")	
	#print(bat_liv_list)
	
# converto la lista in un array di booleani per poter controllare se il valore è sotto la soglia 

	y = np.array(bat_liv_list)
	floatArray = y.astype(float)
	print (floatArray) 
	floatArray = list(reversed(floatArray)) 

	print("\n"" ** Check Battery Threshold: ** ""\n")

	mid_bat_thre = 50.0
	min_bat_thre = 30.0
	BATTERY_30 = False
	BATTERY_50 = False
	battery_trace = []

	lineLen = len(bat_liv_list)
	for i in range(lineLen):
		if floatArray[i] > mid_bat_thre:
 			BATTERY_30 = True
 			BATTERY_50 = True
 			BATTERY_STATE = [BATTERY_30,BATTERY_50]
 			#print(BATTERY_STATE)
 			battery_trace.append(BATTERY_STATE)
		
		elif floatArray[i] > min_bat_thre and floatArray[i] < mid_bat_thre:
 			BATTERY_30 = True
 			BATTERY_50 = False
 			BATTERY_STATE = [BATTERY_30,BATTERY_50]
 			#print(BATTERY_STATE)
 			battery_trace.append(BATTERY_STATE)

		elif floatArray[i] < min_bat_thre:
			BATTERY_30 = False
			BATTERY_50 = False
			BATTERY_STATE = [BATTERY_30,BATTERY_50]
			#print(BATTERY_STATE)
			battery_trace.append(BATTERY_STATE)

	print('Json trace: \n')
	y = json.dumps(battery_trace)
	print(y)
	print('\n')

# le due righe qui sotto producono un file json contenente la traccia

	with open("bat_trace.json", "w") as outfile:
		json.dump(battery_trace, outfile)





# entering except block
except :
	print("\nThe file doesn't exist!")