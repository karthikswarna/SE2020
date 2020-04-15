# import pdfkit
import jinja2

num_of_gen = 5

# Read file.
file = open("output_param", 'r')
lines = file.readlines()
i = 0
for line in lines:
    if line == "  ====  ===  ====  =======  =======  ====\n":
        break
    
    words = line.split(' ')
    if(len(words[1].split(',')) == 1):
        i = i + 1
    else:
        break

text1 = lines[:i]       # Values for single parameter.
lines = lines[i:]

i = 0
for line in lines:
    if line == "  ====  ===  ====  =======  =======  ====\n":
        break
    else:
        i = i + 1

text2 = lines[:i]       # Values for combination of parameters.

text3 = lines[i + 1:]   # Fitness scores.
text3 = [line.split() for line in text3]
text4 = text3[num_of_gen * len(text1):] # Fitness score for generations with combinations of parameters changing.
text3 = text3[:num_of_gen * len(text1)] # Fitness score for generations single changing parameter.

# Loading the template with text.
templateLoader = jinja2.FileSystemLoader(searchpath = "../templates")
templateEnv = jinja2.Environment(loader = templateLoader)
TEMPLATE_FILE = "report.txt"
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(text1 = text1, text2 = text2, text3 = text3, text4 = text4, 
            num_of_gen = num_of_gen, num_of_param = len(text1), num_of_combo = len(text2))

# creating html file with the template text.
html_file = open("report" + '.html', 'w')
html_file.write(outputText)
html_file.close()

# pdfkit.from_file('report.html', 'report.pdf')
