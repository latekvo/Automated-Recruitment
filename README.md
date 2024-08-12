# Recruitment management toolkit

Audio-visual enabled recruitment framework, which assesses candidates automatically based on their responses, skill assessment, and their CV.

### Abstract:

Current candidate pool is littered with spam.
This is caused by over-reliance on CVs and other market factors, which can be mitigated by introducing novel assessment methods.
By reducing the candidate pool by 90%, we can extract those, who are worth reviewing manually, and automatically but organically reject those, who wouldn't meet skill expectations otherwise.

### Requirements

- Make sure to have tesseract ocr command line utility installed on you machine.
- Use provided conda environment to download all required packages.

### Running:

#### Prepare: 
- `conda env create`
- `conda activate AutomatedRecruitment`

#### CV analysis
- `python test_cv.py`

#### Video analysis
- `python test_interview.py`

#### Start webui
- `npm install`
- `npm start`

---
### Clauses:

This software is provided under Apache 2 license.

For further details, see attached "LICENSE" file.

```commandline
Some of the template files are provided thanks to https://resumeworded.com/

None of the provided sample files are a part of this software, 
and are only provided as a supplementary reference data.
None of the provided sample files are of completely original production.
I do not claim the ownership of the provided data samples.
```

#### Except as represented in this agreement, all work product by Developer is provided ​“AS IS”. Other than as provided in this agreement, Developer makes no other warranties, express or implied, and hereby disclaims all implied warranties, including any warranty of merchantability and warranty of fitness for a particular purpose.