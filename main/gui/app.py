import os
from flask import *  
app = Flask(__name__)  
import jinja2


@app.route('/')  
def upload():  
    return render_template("index.html")  
 
@app.route('/success', methods = ['POST'])  
def success():

    Cur_dir = os.getcwd()
    print(Cur_dir)
    wrapper_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    print(wrapper_dir)
    os.chdir(Cur_dir)
    

    if request.method == 'POST':  
        # f = request.files['file']
        # f.save(f.filename)  
        
        print("------------------------------------------------------")

        new_variables = request.form.getlist('inputer')

        new_variables = [int(i) for i in new_variables]

        print(new_variables)
        
        print("------------------------------------------------------")

        os.chdir(wrapper_dir)

        # cmd2 = 'python Refactor.py'

        # os.system(cmd2)

        cmd = 'python wrapper.py '+str(len(new_variables))

        for k in new_variables:
            cmd = cmd + ' ' + str(k)

        os.system(cmd)
        
        cmd1 = 'python temp.py'

        os.system(cmd1)

        cmd2 = 'copy report.html gui/templates'

        os.system(cmd2)
        
## Karthik
        # file = open("output_param", 'r')
        # lines = file.readlines()
        # i = 0
        # for line in lines:
        #     words = line.split(' ')
        #     if(len(words[1].split(',')) == 1):
        #         i = i + 1
        #     else:
        #         break
        # text1 = lines[:i]
        # text2 = lines[i:]

        # # Loading the template with text.
        # templateLoader = jinja2.FileSystemLoader(searchpath = "../templates")
        # templateEnv = jinja2.Environment(loader = templateLoader)
        # TEMPLATE_FILE = "report.txt"
        # template = templateEnv.get_template(TEMPLATE_FILE)
        # outputText = template.render(text1 = text1, text2 = text2)

        # # creating html file with the template text.
        # html_file = open("report" + '.html', 'w')
        # html_file.write(outputText)
        # html_file.close()

        os.chdir(Cur_dir)
        # return "<a>Not a valid python file</a>"
        return render_template("report.html", name = 'f.filename')  
        
        # return "<a>Not a valid python file</a>"

@app.route('/refactor', methods = ['POST'])  
def refactor():

    Cur_dir = os.getcwd()
    print(Cur_dir)
    wrapper_dir = os.path.normpath(os.getcwd() + os.sep + os.pardir)
    print(wrapper_dir)
    os.chdir(Cur_dir)
    

    if request.method == 'POST':  
        f = request.files['file']
        f.save(f.filename)  
        
        os.chdir(wrapper_dir)

        cmd2 = 'python Refactor.py'

        kline = open('variable').readlines()


        os.chdir(Cur_dir)
        # return "<a>Not a valid python file</a>"
        return render_template("refactor.html", name = f.filename, variables = kline, num = len(kline))  
        
        # return "<a>Not a valid python file</a>"
  
if __name__ == '__main__':  
    app.run(debug = True)  