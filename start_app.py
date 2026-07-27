"""Start the Streamlit app on an available port."""
import subprocess, sys, time, os, urllib.request

# Kill old processes
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
               capture_output=True, shell=True)
time.sleep(2)

# Start server
proc = subprocess.Popen(
    [sys.executable, '-m', 'streamlit', 'run', 
     os.path.join(os.getcwd(), 'streamlit_app', 'app.py'),
     '--server.port', '8524', '--server.headless', 'true'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    creationflags=subprocess.CREATE_NO_WINDOW
)

with open('streamlit.pid', 'w') as f:
    f.write(str(proc.pid))
print(f'Started PID: {proc.pid}')

time.sleep(6)

if proc.poll() is not None:
    print(f'Process died with code {proc.returncode}')
    sys.exit(1)

try:
    resp = urllib.request.urlopen('http://localhost:8524')
    print(f'HTTP {resp.status} - APP RUNNING on http://localhost:8524')
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
