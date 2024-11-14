import os
import subprocess as sp

# sp.run(["npm", "run", "build"], cwd=os.path.join(os.getcwd(), "frontend"), shell=True)
sp.Popen(["serve", "dist"], cwd=os.path.join(os.getcwd(), "frontend"), shell=True)
sp.Popen(["python", "app.py"], cwd=os.path.join(os.getcwd(), "backend"), shell=True)