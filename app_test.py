import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === CONFIGURATION ===
resume_folder = r"D:\00 Ap_Resume"
job_description_text = "Looking for a Data Analyst with strong Python, SQL, and Power BI skills."
app_url = "http://127.0.0.1:5000"  # Change if hosted elsewhere

# === Prepare resume file paths ===
resume_files = [
    os.path.join(resume_folder, f)
    for f in os.listdir(resume_folder)
    if f.lower().endswith(('.pdf', '.docx'))
]
file_paths = "\n".join(resume_files)

# === Start WebDriver ===
driver = webdriver.Chrome()
driver.get(app_url)
driver.maximize_window()

try:
    wait = WebDriverWait(driver, 10)

    # Enter job description
    job_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "textarea")))
    job_input.send_keys(job_description_text)

    # Upload files
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys(file_paths)

    time.sleep(2)

    # Click "Submit"
    submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]")
    submit_btn.click()
    print("✅ Submitted successfully.")
    time.sleep(2)

    # Click "Top Five Resumes"
    top_five_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Top Five Resumes')]")
    top_five_btn.click()
    print("✅ Clicked Top Five Resumes.")
    time.sleep(2)

    # Click "All Resumes"
    all_resumes_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'All Resumes')]")
    all_resumes_btn.click()
    print("✅ Clicked All Resumes.")
    time.sleep(2)

    # Click "Download Top 5 (ZIP)"
    download_top5_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Download Top 5 (ZIP)')]")
    download_top5_btn.click()
    print("✅ Clicked Download Top 5 (ZIP).")
    time.sleep(2)

    # Click "Download Remaining Emails"
    download_emails_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Download Remaining Emails')]")
    download_emails_btn.click()
    print("✅ Clicked Download Remaining Emails.")

    print("🎉 Test completed successfully!")

finally:
    time.sleep(5)
    driver.quit()
