# Team R3 - Automated Resume Endorser

## Abstract
In order to apply for any kind of job the primary thing one person needs is the Resume.

A person is able to add anything he/she wants in their resume, but when the company goes through it, they can’t validate it,
they just have to assume all the things written on the resume are true and shortlist them based on that.

Thus,many people can get through the successive rounds just by mentioning the required keywords without possessing any real skillset.
The progression  of the project is to provide a solution for the represented problem statement That is to “Validate the Resume”. 

By conducting a test, providing and storing scores in a database, generating QR code in the resume through which the company can access 
the score and other information hence the validation authenticates or
provides some kind of credibility to the resume stating he/she is skilled in.

## SYSTEM OVERVIEW
Once the resume is uploaded to our system , it will extract the text in the resume using tesseract OCR and
feed the extracted resume to our TF-IDF model which will determine the domain of the person who uploaded
the resume, then a test link will be sent to the uploader’s email ( email Id will also be extracted from the resume ,
if email Id not present in the resume then it is considered to be invalid) , the uploader will take up the test through
the link and the results will be stored in our database ,all the above validated information are stored in the
system’s database.

A QR code will be generated and given with the
resume which upon scanning will show the domain and
all the validated data from the resume.

### 1) UPLOAD RESUME

Candidate has to upload his/her resume in the web.

### 2) KEYWORD EXTRACTION

Keywords from the resume are extracted using ML.

### 3) KEYWORD VALIDATION

Keywords are validated by making the candidate to attend a test based on the extracted keyword.

### 4) SCORE PROVISION

Based on the relevance of the job description and skillset mark weightage will be assigned for each question.

### 5) QR CODE GENERATION

A QR code will be generated and added with the resume which on scanning will provide the information of the validated content from the resume.


## Modules of the System:

### MODULE 1 – Text extraction using tesseract OCR (Input: Uploader’s resume)

### MODULE 2 – Term Frequency – Inverse Document Frequency NLP Model (Input: Output of module 1)

### MODULE 3 – Classification of domain using k-NN Algorithm, (Input: Output of module 2)

### MODULE 4 – Text similarity validation with correct and provided answer, (Input: Output of module 2 and module 3)

### MODULE 5 – User Interface (Input: Output of module 1, module 2, and module3 and module 4)


# Team Members
## Aravind R 
## Nikhil R 
## Vishnu Prasath R
