import base64
import requests
import struct

SAPI_HOME = "https://na-west-1.cloud.dwavesys.com/sapi/v2"
SAPI_TOKEN = "DEV-b7ef410cdf48095080bad36ae09386aaf23d4f67"

session = requests.Session()
session.headers = {'X-Auth-Token': SAPI_TOKEN, 'Content-type': 'application/json'}

r4 = session.get(f"{SAPI_HOME}/problems/{'1d024c4c-d678-4d94-ac1d-0dcebe3583b0'}/answer")
r4 = r4.json()

print(r4)

qpu_access_time = r4['answer']['timing']['qpu_access_time']
qpu_sampling_time = r4['answer']['timing']['qpu_sampling_time']
qpu_programming_time = r4['answer']['timing']['qpu_programming_time']
print(qpu_access_time)
print(qpu_sampling_time)
print(qpu_programming_time)

energies = base64.b64decode(r4['answer']['energies'])
energies_decode = struct.unpack('<' + ('d' * (len(energies) // 8)), energies)

print(f"Found lowest energy {min(energies_decode)} in {qpu_access_time} microseconds.")

num_oc = base64.b64decode(r4['answer']['num_occurrences'])
num_oc_decode = struct.unpack('<' + ('d' * (len(num_oc) // 8)), num_oc)
print(num_oc_decode)