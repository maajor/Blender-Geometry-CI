import os
import json
import argparse

def main(directory):
    geos = []
    for filename in os.listdir(os.path.join(directory,"geos")):
        entry = {}
        entry["filename"] = os.path.join("geos", filename)
        geos.append(entry)
    with open(os.path.join(directory,"geomanifest.json"), 'w') as f:
        json.dump(geos, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    _, all_arguments = parser.parse_known_args()
    parser.add_argument('-d', '--directory', help="relative directory", default="")
    parsed_script_args, _ = parser.parse_known_args(all_arguments)
    main(parsed_script_args.directory)