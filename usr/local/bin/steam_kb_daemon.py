#!/usr/bin/env python3
import os
import subprocess
import time

STATE_FILE = os.path.expanduser("~/.config/onboard_kb_state.bool")
TARGET_SCRIPT = "/usr/local/bin/launcher_action.sh"

# Target the Onboard virtual keyboard window and process identifiers
KB_WINDOW_NAMES = ["onboard"]


def get_state():
  if not os.path.exists(STATE_FILE):
    set_state(False)
    return False
  with open(STATE_FILE, "r") as f:
    return f.read().strip() == "True"


def set_state(val):
  os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
  with open(STATE_FILE, "w") as f:
    f.write(str(val))


def check_keyboard_active():
  try:
    output = subprocess.check_output(
        ["xdotool", "search", "--name", ".*"], text=True, stderr=subprocess.DEVNULL
    )
    for wid in output.strip().split("\n"):
      if not wid:
        continue
      wname = subprocess.check_output(
          ["xdotool", "getwindowname", wid], text=True, stderr=subprocess.DEVNULL
      ).lower()
      if any(token in wname for token in KB_WINDOW_NAMES):
        return True
  except Exception:
    try:
      ps = subprocess.check_output(["ps", "-e", "-o", "comm="], text=True)
      if "onboard" in ps.lower():
        return True
    except Exception:
      pass
  return False


def main():
  was_open = False
  print("Onboard Keyboard Daemon started...")

  while True:
    is_open = check_keyboard_active()

    # Detect transition from Open -> Closed
    if was_open and not is_open:
      current_state = get_state()
      new_state = not current_state
      set_state(new_state)

      print(f"Onboard closed event caught. State toggled to: {new_state}")

      if new_state:  # Fires every alternate close event
        print("Launching target script...")
        subprocess.run([TARGET_SCRIPT])

    was_open = is_open
    time.sleep(0.5)


if __name__ == "__main__":
    main()
