import json
import sys
import easygui
from Tkinter import Tk
from subprocess import Popen, PIPE


def main():
    name = "LOLBind"

    if sys.platform == "darwin":
        Tk().destroy()
        # Next we activate it
        Popen(['osascript', '-e', 'tell application "Python" to activate'])

        key_settings_path = "/Applications/League of Legends.app/Contents/LoL/Config/PersistedSettings.json"
    elif sys.platform == "win32" or sys.platform == "win64":
        key_settings_path = "C:\Riot Games\League of Legends\Config\PersistedSettings.json"
    else:
        easygui.msgbox("Unsupported operating system. LOLBind will now quit.", name)
        sys.exit(0)

    with open(key_settings_path, "r") as f:
        jo = json.load(f)
        ks = jo["files"][1]["sections"][0]["settings"]
        i = 0
        for k in ks:
            if k["name"] == "evtChampMasteryDisplay":
                cont = easygui.msgbox("Mastery Emote currently bound to %s.\nPress okay to continue." %
                               jo["files"][1]["sections"][0]["settings"][i]["value"], name)
                if cont == "OK":
                    keys_to_bind = easygui.multchoicebox("Select keys you want to bind to Mastery Emote",
                                                         title=name, choices=["q", "w", "e", "r", "d", "f"])
                    mastery_key = "[Ctrl][6]"
                    if keys_to_bind is not None:
                        for key in keys_to_bind:
                            mastery_key = ("[%s]," % key) + mastery_key
                    jo["files"][1]["sections"][0]["settings"][i]["value"] = mastery_key
                break
            i += 1

    if cont == "OK":
        with open(key_settings_path, "w") as f:
            json.dump(jo, f)
            if easygui.msgbox("Sucessfully changed mastery keys to %s.\nTo change bound keys click okay." % mastery_key,
                              name) == "OK":
                f.close()
                main()
            else:
                sys.exit(0)
    else:
        sys.exit(0)


if __name__ == '__main__':

    main()
