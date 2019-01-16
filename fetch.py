from bs4 import BeautifulSoup
import urllib.request
import json
import sys, time, os

Max_Sol = 10000

print('Enter Codeforces_handle : ')
handle = input().strip()

extensions = {'C++': 'cpp', 'GNU C++14': 'cpp', 'GNU C++17': 'cpp', 'Python 3': 'py', 'GNU C++11': 'cpp', 'C': 'c',
              'Java': 'java', 'Python': 'py', 'Delphi': 'dpr', 'FPC': 'pas', 'C#': 'cs'}

SOURCE_CODE_URL = 'http://codeforces.com/contest/{contestId}/submission/{sub_id}'

REQUEST_URL = 'http://codeforces.com/api/user.status?handle={handle}&from=1&count={count}'.format(handle=handle,
                                                                                                  count=Max_Sol)

print('Fetching user status : ', REQUEST_URL)

dic = json.loads(urllib.request.urlopen(REQUEST_URL).read())

if dic["status"] == "FAILED":
    print(r"Solutions cann't be fetched")
    exit(0)

submissions = [sub for sub in dic["result"] if sub["verdict"] == "OK"]

base_dir = 'Codes_{handle}/'.format(handle=handle)

if not os.path.exists(base_dir):
    os.makedirs(base_dir)

print('Fetching %d submissions' % len(submissions))

start = time.time()

for submission in submissions:
    try:
        contestId, sub_id = submission["contestId"], submission["id"]
        prob_name, prob_type = submission["problem"]["name"], submission["problem"]["index"]
        language = submission["programmingLanguage"]
    except:
        pass

    FULL_SOURCE_CODE_URL = SOURCE_CODE_URL.format(contestId=contestId, sub_id=sub_id)
    print('Fetching submission: %s' % FULL_SOURCE_CODE_URL)
    sub_info = urllib.request.urlopen(FULL_SOURCE_CODE_URL).read()
    soup = BeautifulSoup(sub_info, 'html.parser')
    submission_text = soup.find('pre', id='program-source-text')

    if submission_text is None:
        print('Could not fetch %d sulution', sub_id)
        continue

    source_code = submission_text.text.replace('\r', '')

    ext = extensions[language]

    line_comment = ''
    if ext == 'py':
        line_comment = '#'
    else:
        line_comment = r'//'

    for x in ['\\', '/', '|', '?', ':', '\"', '<', '>', '*']:
        prob_name = prob_name.replace(x, '')

    file_name = str(contestId) + ' ' + prob_type + ' ' + prob_name + '.' + ext
    file = open(base_dir + file_name, 'w')
    file.write(line_comment + ' ' + 'http://codeforces.com/contest/' + str(contestId) + '/problem/' + prob_type + '\n')
    file.write(source_code)
    file.close()

end = time.time()

duration = int(end - start)
print('Finished in %d min %d secs' % (duration / 60, duration % 60))