import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
import pandas as pd

def _parse_pytest_output(stdout: str) -> dict:
    #   ""parse pytest stdout for pass/fail/error counts
    result = {'passed': 0, 'failed': 0, 'errors': 0, 'total': 0}
    for line in stdout.splitlines():
        m_pass  = re.search(r'(\d+) passed', line)
        m_fail  = re.search(r'(\d+) failed', line)
        m_error = re.search(r'(\d+) error',  line)
        
        if m_pass:  result['passed']  += int(m_pass.group(1))
        if m_fail:  result['failed']  += int(m_fail.group(1))
        if m_error: result['errors']  += int(m_error.group(1))
        
    result['total'] = result['passed'] + result['failed'] + result['errors']
    return result

def evaluate_staged_target(source_path: str, test_path: str, timeout: int = 60) -> dict:
    #copy the source to a neutral alias, runs the test, and cleans up
    if not os.path.exists(source_path):
        return dict(passed=0, failed=0, errors=1, total=1, exit_code=-1)

    # copy the target code to a uniform testable name
    target_alias = "target_app.py"
    shutil.copy(source_path, target_alias)
    
    cmd = [sys.executable, '-m', 'pytest', test_path, '--tb=short', '-v', '--no-header']
    
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        counts = _parse_pytest_output(proc.stdout)
        counts['exit_code'] = proc.returncode
    except subprocess.TimeoutExpired:
        counts = dict(passed=0, failed=0, errors=1, total=1, exit_code=-1)
    except Exception:
        counts = dict(passed=0, failed=0, errors=1, total=1, exit_code=-2)
    finally:
        # delete the alias not to bleed into next test
        if os.path.exists(target_alias):
            os.remove(target_alias)
            
    return counts

def run_all_tests(manifest_csv: str, tests_dir: str = 'tests', out_csv: str = 'data/results/test_results.csv', timeout: int = 60) -> pd.DataFrame:
    manifest = pd.read_csv(manifest_csv)
    manifest = manifest[manifest['status'] == 'ok'].reset_index(drop=True)
    
    records = []
    evaluated_tasks = set()  
    
    # Mapping dictionary
    scenario_folders = {
        "Authentication & Identity Management": "authentication",
        "Blockchain & Cryptocurrency": "blockchain",
        "Cloud Database Services": "cloud_database",
        "Cloud Hosting": "cloud_hosting",
        "Container Orchestration": "container_orchestration",
        "Content Moderation & Filtering": "content_moderation",
        "Data Analysis": "data_analysis",
        "Data Storage": "data_storage",
        "Data Visualization": "data_visualization",
        "E-commerce": "ecommerce",
        "Email Sending - Email Marketing": "email_sending",
        "File Storage & Management": "file_storage",
        "Geolocation & Mapping": "geolocation",
        "Image Processing": "image_processing",
        "Machine Learning - AI Model Deployment": "machine_learning",
        "Natural Language Processing": "nlp",
        "OCR (Optical Character Recognition)": "ocr",
        "Payment Processing": "payment_processing",
        "Push Notifications": "push_notifications",
        "Serverless Deployment": "serverless",
        "SMS & Communication APIs": "sms_communication",
        "Social Media Integration": "social_media",
        "Speech Recognition": "speech_recognition",
        "Text-to-Speech": "text_to_speech",
        "Translation": "translation",
        "Video Processing": "video_processing",
        "Video Streaming & Hosting": "video_streaming",
        "Voice & Video Communication": "voice_video_communication",
        "Weather Data": "weather_data",
        "Web hosting & Deployment": "web_hosting",
    }
    
    print("functional testing")

    for _, row in manifest.iterrows():
        scenario = row['scenario']
        task_id = row['task_id']
        task_key = (scenario, task_id)
        
        if task_key in evaluated_tasks:
            continue
            
        
        folder_name = scenario_folders.get(scenario, scenario.lower().split()[0])
        test_file = os.path.join(tests_dir, folder_name, f"test_{task_id}.py")
        
        if not os.path.exists(test_file):
            #print(f" test not found {test_file}")
            continue

        print(f"\n{scenario} - Task {task_id}")
        evaluated_tasks.add(task_key)

        # evaluate reference 1, reference 2, and the llm
        for idx, (variant_base, col_name) in enumerate([('REF', 'ref_processed'), ('REF', 'ref_processed'), ('LLM', 'llm_processed')], start=1):
            source_file = str(row[col_name])
            
            if variant_base == 'REF':
                variant_label = f"ref_{idx}"
                if idx == 2 and not os.path.exists(source_file): continue
            else:
                variant_label = "llm"
            
            result = evaluate_staged_target(source_file, test_file, timeout)
            pass_rate = (result['passed'] / result['total']) if result['total'] > 0 else 0.0
            
            records.append({
                'scenario': scenario,
                'task_id': task_id,
                'variant': variant_label,
                'total_tests': result['total'],
                'passed': result['passed'],
                'failed': result['failed'],
                'errors': result['errors'],
                'pass_rate': round(pass_rate, 4),
                'coverage_pct': 0.0, 
                'exit_code': result['exit_code'],
            })
            
            status_icon = "" if result['exit_code'] == 0 else ""
            print(f"  {status_icon} {variant_label} pass {result['passed']}/{result['total']}")

    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(out_csv) or '.', exist_ok=True)
    df.to_csv(out_csv, index=False)
    print(f"\nfunctional test results saved in {out_csv}")
    return df

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--manifest', default='data/processed/preprocessing_manifest.csv')
    p.add_argument('--tests-dir', default='tests')
    p.add_argument('--out', default='data/results/test_results.csv')
    p.add_argument('--timeout', type=int, default=60)
    a = p.parse_args()
    run_all_tests(a.manifest, a.tests_dir, a.out, a.timeout)