# import pdfkit
import jinja2

# Read file.
file = open("output_param", 'r')
lines = file.readlines()
i = 0
for line in lines:
    words = line.split(' ')
    if(len(words[1].split(',')) == 1):
        i = i + 1
    else:
        break
text1 = lines[:i]
text2 = lines[i:]

# Loading the template with text.
templateLoader = jinja2.FileSystemLoader(searchpath = "../templates")
templateEnv = jinja2.Environment(loader = templateLoader)
TEMPLATE_FILE = "report.txt"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(text1 = text1, text2 = text2)

# creating html file with the template text.
html_file = open("report" + '.html', 'w')
html_file.write(outputText)
html_file.close()

# pdfkit.from_file('report.html', 'report.pdf')
