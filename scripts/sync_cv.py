"""Bring the site in line with the CV in one step.

    python scripts/sync_cv.py            # export, rebuild, regenerate, check
    python scripts/sync_cv.py --check    # only say whether the site is behind the CV

The CV (Word original in OneDrive Career/CV/) is the source; the site follows it.
A sync:

  1. takes the newest CV .docx in the CV folder,
  2. exports it to PDF with Word ("Curriculum Vitae_YJYOO_<Mon>_<YYYY>.pdf", this
     month; an earlier month's PDF stays as it was),
  3. writes the public copy without the phone number (build_public_cv.py),
  4. regenerates the publication list from it (update_publications.py, which ends
     by checking the whole site against the CV: papers, positions, degrees,
     fellowships and awards, funded projects),
  5. records which .docx the site now reflects, in scripts/cv_source.json.

It never commits or pushes. Read `git diff`, then commit.

--check compares the newest .docx with cv_source.json. The Simulations
SessionStart hook runs it with --quiet, so a CV edited without a sync is
announced at the start of the next session instead of being found by a reader.
"""

import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
CV_DIR = r"C:\Users\YJ\OneDrive\Career\CV"
STATE = os.path.join(HERE, "cv_source.json")
WORD_TIMEOUT_S = 150   # Word COM has hung before (2026-09-19); never wait forever


def latest_docx():
    names = [n for n in os.listdir(CV_DIR)
             if n.lower().endswith(".docx") and not n.startswith("~$")]
    if not names:
        raise SystemExit(f"no CV .docx in {CV_DIR}")
    return max((os.path.join(CV_DIR, n) for n in names), key=os.path.getmtime)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def check(quiet):
    docx = latest_docx()
    state = load_state()
    if state.get("sha256") == sha256(docx):
        if not quiet:
            print(f"in sync: site reflects {os.path.basename(docx)} (synced {state.get('synced')})")
        return 0
    modified = datetime.datetime.fromtimestamp(os.path.getmtime(docx)).strftime("%Y-%m-%d %H:%M")
    since = f"last sync {state['synced']}" if state.get("synced") else "never synced"
    print(f"CV changed after the homepage was synced ({os.path.basename(docx)}, edited {modified}; "
          f"{since}): python {os.path.join(SITE, 'scripts', 'sync_cv.py')}")
    return 1


def export_pdf(docx, pdf):
    """Word COM on a local copy, read-only, under a timeout (the pattern that works)."""
    tmp = tempfile.mkdtemp(prefix="cv_sync_")
    src, out = os.path.join(tmp, "cv.docx"), os.path.join(tmp, "cv.pdf")
    shutil.copy2(docx, src)
    ps = f"""
$job = Start-Job -ScriptBlock {{
  param($src, $out)
  $w = New-Object -ComObject Word.Application
  $w.Visible = $false; $w.DisplayAlerts = 0
  $doc = $w.Documents.Open($src, $false, $true, $false)
  $doc.ExportAsFixedFormat($out, 17)
  $doc.Close(0); $w.Quit()
}} -ArgumentList '{src}', '{out}'
if (Wait-Job $job -Timeout {WORD_TIMEOUT_S}) {{ Receive-Job $job }} else {{ Stop-Job $job; exit 3 }}
"""
    r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                       capture_output=True, text=True, timeout=WORD_TIMEOUT_S + 60)
    if r.returncode == 3 or not os.path.exists(out):
        raise SystemExit(f"Word did not export the PDF within {WORD_TIMEOUT_S} s "
                         f"(exit {r.returncode}). Open the .docx in Word, Save As PDF to\n"
                         f"  {pdf}\nthen run: python scripts/build_public_cv.py \"{pdf}\" "
                         f"--no-check && python scripts/update_publications.py")
    shutil.copy2(out, pdf)
    shutil.rmtree(tmp, ignore_errors=True)


def run(step, *args):
    print(f"\n=== {step} {' '.join(args)} ===", flush=True)
    r = subprocess.run([sys.executable, os.path.join(HERE, step), *args])
    if r.returncode != 0:
        raise SystemExit(f"{step} failed (exit {r.returncode}); cv_source.json not updated")


def sync():
    docx = latest_docx()
    digest = sha256(docx)
    today = datetime.date.today()
    pdf = os.path.join(CV_DIR, f"Curriculum Vitae_YJYOO_{today:%b}_{today:%Y}.pdf")
    print(f"source : {docx}\nexport : {pdf}", flush=True)
    export_pdf(docx, pdf)
    run("build_public_cv.py", pdf, "--no-check")
    run("update_publications.py")
    json.dump({"docx": os.path.basename(docx), "sha256": digest,
               "pdf": os.path.basename(pdf), "synced": today.isoformat()},
              open(STATE, "w", encoding="utf-8"), indent=1)
    print(f"\nrecorded {os.path.basename(STATE)}. Changed files:")
    subprocess.run(["git", "-C", SITE, "status", "--short"])
    print("Nothing is committed. Review with git diff, then commit and push.")


if __name__ == "__main__":
    if "--check" in sys.argv:
        sys.exit(check(quiet="--quiet" in sys.argv))
    sync()
