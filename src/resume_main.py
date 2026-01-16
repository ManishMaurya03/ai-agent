import pandas as pd
from reader import get_resume_files, read_job_description
from extractor import extract_resume_text
from prompt import build_resume_screening_prompt
from evaluator import evaluate_resume

RESUME_FOLDER = "/Users/manishmaurya/Desktop/OpenAIApplications/FirstOpenAIProject/resume"
JD_FILE = "job_description.txt"
OUTPUT_FILE = "/Users/manishmaurya/Desktop/OpenAIApplications/FirstOpenAIProject/output/results.csv"

def main():
    resumes = get_resume_files(RESUME_FOLDER)
    job_desc = read_job_description(JD_FILE)

    results = []

    for file in resumes:
        print(f"\nProcessing: {file}")

        resume_text = extract_resume_text(file)
        # Print resume text BEFORE sending to LLM
        print("------ EXTRACTED RESUME TEXT (Preview) ------\n")
        print(resume_text[:3000])   # Print first 3000 characters
        print("\n-------------------------------------------\n")

        prompt = build_resume_screening_prompt(resume_text, job_desc)

        evaluation = evaluate_resume(prompt)

        if evaluation:
            evaluation["file_name"] = file
            results.append(evaluation)

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Rank by score
    df = df.sort_values(by="match_score", ascending=False)

    # Save to CSV
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\nResume Screening Completed.")
    print(f"Results saved to: {OUTPUT_FILE}")

    # Show Top 3
    print("\nTop Candidates:")
    print(df[["candidate_name", "match_score", "classification","matched_skills","missing_skills","recommendation"]].head(6))

 

if __name__ == "__main__":
    main()