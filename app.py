from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)

LANGUAGES = {
    "python": "python3",
    "javascript": "node",
    "bash": "bash",
    "c": "gcc",
    "cpp": "g++",
    "java": "javac",
    "ruby": "ruby",
    "php": "php",
    "go": "go run",
    "perl": "perl",
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code')
    language = data.get('language')
    
    filename = f'code.{language}'
    output = ""

    try:
        if language in ["c", "cpp"]:
            source_file = f"code.{language}"
            executable = "code_executable"
            with open(source_file, 'w') as f:
                f.write(code)
            
            compile_cmd = [LANGUAGES[language], source_file, '-o', executable]
            subprocess.check_output(compile_cmd, stderr=subprocess.STDOUT, timeout=10, universal_newlines=True)
            
            output = subprocess.check_output([f'./{executable}'], stderr=subprocess.STDOUT, timeout=5, universal_newlines=True)
            os.remove(source_file)
            os.remove(executable)

        elif language == "java":
            source_file = "Main.java"
            class_name = "Main"
            with open(source_file, 'w') as f:
                f.write(code)

            compile_cmd = [LANGUAGES[language], source_file]
            subprocess.check_output(compile_cmd, stderr=subprocess.STDOUT, timeout=10, universal_newlines=True)
            
            output = subprocess.check_output(["java", class_name], stderr=subprocess.STDOUT, timeout=5, universal_newlines=True)
            os.remove(source_file)
            os.remove(f"{class_name}.class")

        else:
            with open(filename, 'w') as f:
                f.write(code)

            command = LANGUAGES[language].split()
            command.append(filename)
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=5, universal_newlines=True)
            os.remove(filename)

    except subprocess.CalledProcessError as e:
        output = e.output
    except Exception as e:
        output = str(e)

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)
