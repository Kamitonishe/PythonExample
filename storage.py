import argparse
import os
import tempfile
import json

parser = argparse.ArgumentParser()
parser.add_argument("--key", help=" key argument")
parser.add_argument("--val", help=" value argument")
args = parser.parse_args()

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')

if args.val:
    with open(storage_path, 'a') as f:
        f.write(json.dumps({
    'key': args.key,
    'val': args.val
        }) + '\n')

else:
    if not os.path.isfile(storage_path):
        f = open(storage_path, 'w')
        f.close()

    answer = []
    with open(storage_path, 'r') as f:
        for line in f:
            from_json_line = json.loads(line.strip())
            if from_json_line['key'] == args.key:
                answer.append(from_json_line['val'])


    print(', '.join(answer))




