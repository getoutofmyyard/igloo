with open('.\\installCmds.txt','r') as file:
	read_file = file.read()
	split_file = read_file.split('\n')
	for line in split_file:
		split_line = line.split('\'')
		print(split_line[0])
		
