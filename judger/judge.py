import tempfile
import os, sys
import subprocess

judge_config = {
    'time_limit': 10 * 60 * 60,    # time limit in seconds, set to 0 if no limit
    'entry_file': './main.sh',     # entry file
    'final_score': './score.txt',  # the final score, in integer
    'submit_logs': True,
    'url_host': 'http://localhost:8080/'
}

def get_submission_detail(submission_id, testcase_id):
    # todo: do get query, with token preconfigured, then fill the form
    return {
        'id': 0,
        'problem': {
            'id': 0,
            'problem_files': [
                {'uuid': "abc"}
            ],
            'testcase_id': testcase_id
        },
        'user': {
            'id': 0,
            'student_id': "PB17000232"
        },
        'submit_time': "20101001",
        'submit_files': [
            {'uuid': "abc"}
        ],
        'testcase_files': [
            {'uuid': "abc"}
        ]
    }

def download_file(path, uuid):
    # Download file and store it in path (a dir)
    pass

def push_result(result, submission_id, testcase_id):
    # todo: post to the result, return True on completion
    # result: {}
    return True

def prepare_and_run(detail):
    # make a new folder in /tmp
    with tempfile.TemporaryDirectory() as tmpdirname:
        print('Created temporary directory {}'.format(tmpdirname))
        BASE_PATH = tmpdirname
        TESTCASE_DIR = os.path.join(BASE_PATH, "./testcase")
        PROBLEM_DIR = os.path.join(BASE_PATH, "./problem")
        SUBMIT_DIR = os.path.join(BASE_PATH, "./submit")

        os.mkdir(TESTCASE_DIR)
        os.mkdir(PROBLEM_DIR)
        os.mkdir(SUBMIT_DIR)

        # download all contents in place
        for f in detail['testcase_files']:
            download_file(TESTCASE_DIR, f['uuid'])
        
        for f in detail['problem']['problem_files']:
            download_file(PROBLEM_DIR, f['uuid'])

        for f in detail['submit_files']:
            download_file(SUBMIT_DIR, f['uuid'])

        os.chdir(BASE_PATH)

        # evaluate with time limit
        process = subprocess.Popen(['/bin/bash', os.path.join(TESTCASE_DIR, judge_config['entry_file'])],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
                )
        
        if judge_config['time_limit'] != 0:
            try:
                out, err = process.communicate(timeout=judge_config['time_limit'])
            except subprocess.TimeoutExpired:
                process.kill()
                out, err = process.communicate()
        else:
            out, err = process.communicate()
        

        # push stdout & score to the server
        score_file_path = os.path.join(BASE_PATH, judge_config['final_score'])
        score = None
        if os.path.exists(score_file_path):
            with open(score_file_path, "r") as f:
                score = int(f.read())
        print("Final score: {}".format(score))

        # Grab all logs
        if judge_config['submit_logs']:
            # out.read is expected to be bytes
            log_out = out.decode("utf8")
            log_err = err.decode("utf8")
        else:
            log_out = "Suppressed due to submit_logs in judge configurations"
            log_err = "Suppressed due to submit_logs in judge configurations"

        # Post them back
        result = {
            'score': score,
            'success': True if score is not None else False,
            'log_out': log_out,
            'log_err': log_err
        }

        return result


def judge(submission_id, testcase_id):
    """
    评测某个提交。生成若干SubmissionResult，之后Submission就会被更新。
    """
    # TODO: 对某个提交进行评测
    # Query submission api for a json
    try:
        detail = get_submission_detail(submission_id, testcase_id)
        result = prepare_and_run(detail)
        push_result(result, submission_id, testcase_id)
        return True
    except:
        raise Exception("Comment me on production, but backtraces are useful for debugging")
        print("Unexpected error while processing {}-{}: {}".format(submission_id, testcase_id, sys.exc_info()))
        return False