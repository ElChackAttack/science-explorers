from pathlib import Path

if __name__ == '__main__':

	desired_name = input('Desired html page name >>> ')+'.html'
	print(desired_name)
	my_file = Path("/Users/ricardo/Documents/Science Explorers/Library Management System/Flask_LMS/templates/{}".format(desired_name))
	print(my_file)
	if my_file.is_file():
	# file exists
		print('The file already exists')
	else:
		html_boilerplate = """<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Document</title>
	<link rel="icon" href="static/images/icon.ico">
</head>
<body>
	
</body>
</html>
"""
		f = open(my_file,'w')
		f.write(html_boilerplate)
		f.close()

