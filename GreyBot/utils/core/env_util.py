import dotenv
from pathlib import Path
base = Path(__file__).parent.parent.parent
EnvPat = base / ".env"

def parse_value(value):
    try:
        if value.lower() == ("true" or 1):
            return True
        elif value.lower() == ("false" or 0):
            return False
    except:
        pass
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value

class Enviormental:
    TOKEN = None
    LOGGING_LEVEL = 20
    STREAM_LOGS = True
    def __init__(self):
        self.file = EnvPat
        with open(self.file,'r') as f:
            s = f.read()
        for arg in s.split("\n"):
            print(arg)
            try:
                if len(arg) <= 1:
                    pass
                key, value = arg.split("=")
                setattr(Enviormental, key, parse_value(value))  # int(value) because the value is a string
            except Exception as r:
                pass

    def add_var(self,key,value):
        setattr(Enviormental, key, parse_value(value))
        updated = False
        lines = []
        try:
            with open(self.file, "r") as f:
                for line in f:
                    if line.strip().startswith(f"{key}="):
                        lines.append(f"{key}={value}\n")  # Replace line
                        updated = True
                    else:
                        lines.append(line)
        except FileNotFoundError:
            pass  # File doesn't exist yet
        if not updated:
            lines.append(f"{key}={value}\n")
        with open(self.file, "w") as f:
            f.writelines(lines)

args = Enviormental()
