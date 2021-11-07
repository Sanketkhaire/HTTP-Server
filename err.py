from jinja2 import Template

def generate_error_page(status_code, response_phrase):
	errorPage = Template('''
	<!DOCTYPE html>
	<html>
	<head>
		<title>{{response_phrase}}</title>
	</head>
	<body>
		<h1>{{status_code}} {{response_phrase}}</h1>
		<p>An error occurred</p>
	</body>
	</html>''')

	return errorPage.render(status_code=status_code, response_phrase=response_phrase)




