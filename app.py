from flask import Flask, render_template, request, url_for, redirect
import sys
import os
import warnings
from datetime import datetime
from mentalhealth.crew import Mentalhealth
from mentalhealth.database import JournalDatabase

# Try to import opik, but don't fail if it's not available
try:
    from opik.integrations.crewai import track_crewai
    has_opik = True
except ImportError:
    has_opik = False

# Suppress warnings from pysbd module
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Configure Flask to find templates and static files in the current directory
template_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.dirname(os.path.abspath(__file__))

# Track crewai if opik is available
if has_opik:
    try:
        track_crewai(project_name="mentalhealth")
    except Exception as e:
        print(f"Warning: Could not track crewai: {e}")
app = Flask(__name__, 
           template_folder=template_dir,
           static_folder=static_dir)

# Initialize the database
db = JournalDatabase()

# --- Helper function to read analysis files ---
def get_analysis_content():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    analysis_content = {
        "cbt": "No CBT analysis available",
        "humanistic": "No humanistic analysis available",
        "psychodynamic": "No psychodynamic analysis available",
        "therapy_summary": "No therapy summary available",
        "mood": "No mood analysis available"
    }
    
    # Read CBT response
    try:
        cbt_path = os.path.join(current_dir, 'cbt_response.md')
        if os.path.exists(cbt_path):
            with open(cbt_path, 'r', encoding='utf-8') as f:
                analysis_content["cbt"] = f.read()
                print(f"Successfully read cbt_response.md ({len(analysis_content['cbt'])} characters)")
    except Exception as e:
        analysis_content["cbt"] = f"Error reading cbt_response.md: {e}"
        print(analysis_content["cbt"])
    
    # Read humanistic response
    try:
        humanistic_path = os.path.join(current_dir, 'humanistic_response.md')
        if os.path.exists(humanistic_path):
            with open(humanistic_path, 'r', encoding='utf-8') as f:
                analysis_content["humanistic"] = f.read()
                print(f"Successfully read humanistic_response.md ({len(analysis_content['humanistic'])} characters)")
    except Exception as e:
        analysis_content["humanistic"] = f"Error reading humanistic_response.md: {e}"
        print(analysis_content["humanistic"])
    
    # Read psychodynamic response
    try:
        psychodynamic_path = os.path.join(current_dir, 'psychodynamic_response.md')
        if os.path.exists(psychodynamic_path):
            with open(psychodynamic_path, 'r', encoding='utf-8') as f:
                analysis_content["psychodynamic"] = f.read()
                print(f"Successfully read psychodynamic_response.md ({len(analysis_content['psychodynamic'])} characters)")
    except Exception as e:
        analysis_content["psychodynamic"] = f"Error reading psychodynamic_response.md: {e}"
        print(analysis_content["psychodynamic"])
    
    # Read therapy summary
    try:
        therapy_path = os.path.join(current_dir, 'therapy_response.md')
        if os.path.exists(therapy_path):
            with open(therapy_path, 'r', encoding='utf-8') as f:
                analysis_content["therapy_summary"] = f.read()
                print(f"Successfully read therapy_response.md ({len(analysis_content['therapy_summary'])} characters)")
    except Exception as e:
        analysis_content["therapy_summary"] = f"Error reading therapy_response.md: {e}"
        print(analysis_content["therapy_summary"])
    
    # Read mood analysis
    try:
        mood_path = os.path.join(current_dir, 'mood_analysis.md')
        if os.path.exists(mood_path):
            with open(mood_path, 'r', encoding='utf-8') as f:
                analysis_content["mood"] = f.read()
                print(f"Successfully read mood_analysis.md ({len(analysis_content['mood'])} characters)")
    except Exception as e:
        analysis_content["mood"] = f"Error reading mood_analysis.md: {e}"
        print(analysis_content["mood"])
    
    return analysis_content
# --- End Helper ---

# Function from main.py
def go(topic):
    """
    Run the crew.
    """
    inputs = {
        'topic': topic,
        'current_year': str(datetime.now().year)
    }
    
    try:
        Mentalhealth().crew().kickoff(inputs=inputs)
        print(f"Successfully ran crew with topic: {topic}")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        try:
            print(f"Calling go() function with text: {text[:50]}...")
            go(text)
            # After running go(), get the analysis content
            analysis_content = get_analysis_content()
            print(f"Successfully called go() with text: {text[:50]}...")
            
            # Save the journal entry to the database
            db.save_entry(
                text, 
                analysis_content["therapy_summary"], 
                analysis_content["mood"],
                analysis_content["cbt"],
                analysis_content["humanistic"],
                analysis_content["psychodynamic"]
            )
            
        except Exception as e:
            print(f"Error calling go(): {e}")
            error_msg = f"Error generating analysis: {e}"
            analysis_content = {
                "cbt": error_msg,
                "humanistic": error_msg,
                "psychodynamic": error_msg,
                "therapy_summary": error_msg,
                "mood": error_msg
            }
        
        # Pass analysis content after POST
        return render_template('index.html', 
                              cbt_content=analysis_content["cbt"],
                              humanistic_content=analysis_content["humanistic"],
                              psychodynamic_content=analysis_content["psychodynamic"],
                              therapy_summary_content=analysis_content["therapy_summary"],
                              mood_content=analysis_content["mood"])

    # For GET requests, just render the template with placeholder messages
    placeholder_msg = "Enter your journal entry and click 'Analyze' to receive therapeutic insights."
    return render_template('index.html', 
                          cbt_content=placeholder_msg,
                          humanistic_content=placeholder_msg,
                          psychodynamic_content=placeholder_msg,
                          therapy_summary_content=placeholder_msg,
                          mood_content="Enter your journal entry and click 'Analyze' to receive mood analysis.")

@app.route('/history')
def history():
    """Display all past journal entries"""
    entries = db.get_all_entries()
    return render_template('history.html', entries=entries)

@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    """View a specific journal entry"""
    entry = db.get_entry_by_id(entry_id)
    if entry:
        return render_template('entry.html', entry=entry)
    return redirect(url_for('history'))

@app.route('/clear-entries', methods=['POST'])
def clear_entries():
    """Clear all journal entries"""
    db.clear_all_entries()
    return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(debug=True)
