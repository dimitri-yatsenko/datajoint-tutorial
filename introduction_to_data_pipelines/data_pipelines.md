# Introduction to Data Pipelines


This chapter:
* provides motivation for using data pipelines
* Introduces the concept a data pipeline.  
* Introduces datajoint as a library which facilitates a pipeline
* illustrates a simple experiment of estimating gravity with Galileo



## Your Data Analysis is Messy
Let's face it - many scientists do not focus their efforts onto *how* they organize their data.
Their primary concern is answering interesting questions, so they focus on the physical process of collecting data and developing theory to support its analysis. A typical data management strategy is a collection of file folders with raw data, spreadsheets with notes describing these data, analysis scripts that access these data (likely in MATLAB, Python, R, and Excel), saved intermediate results, and analysis output in the form of plots, tables, etc.

This lack of organization leads to a number of headache-causing scenarios 
If you are reading this book, then you likely have experienced one or more of the following pains:
* Data organization is inconsistent across projects
* Analysis code does not work across datasets
* Analyzing new data is a hassle.
* Sharing raw data and analysis code is difficult with team members.




The data management strategy probably comprises a collection of file folders with raw data recordings, spreadsheets with notes describing these data, analysis scripts that access these data (likely in MATLAB, Python, R, and Excel), saved intermediate results, and analysis output in the form of plots, tables, etc.

## Data pipelines
* Computation graphs


## DataJoint


## A Pipeline
Show the linear model fitting example

### The experiment


### The Graph

### The code walkthrough
```py
def main():
  how_do = True
```

## Questions Reader should be able to answer
* Why is a data pipeline preferable to arbitrary storage?
* 