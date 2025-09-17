from utils.config import get_current_user
from utils.interface_panel import system_panel, signing_panel

if __name__ == "__main__":
    while True:
        if not get_current_user():
            signing_panel()
        panel = system_panel()
        if not panel:
            break