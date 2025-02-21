# Report for assignment 3

This is a template for your report. You are free to modify it as needed.
It is not required to use markdown for your report either, but the report
has to be delivered in a standard, cross-platform format.

## Project

Name: arviz

URL: https://github.com/Rocygel/DD2480-3-arviz

Arviz fork for Assignment 3 in DD2480 course at KTH. Exploratory analysis of Bayesian models with Python

## Onboarding experience

Did it build and run as documented?

used the followind commands:  
conda install -c conda-forge arviz
python setup.py install (in cloned repo)
pip install -r requirements-test.txt


## Complexity

1. What are your results for five complex functions?
   ecdfplot.py with 337 LOC, manual: 25+P, lizard:27
   essplot.py with 295 LOC, manual: 18+P, lizard: 15
   pairplot.py with 291 LOC, manual: 63+P, lizard: 56
   bpvplot.py with 278 LOC, manual: 25+P, lizard: 23

   how we calculated:
      for: 5 edges, 3 node => CC +2 
      if = 3 edges, 2 node => CC+1
         nested if  = +2 edges, +1 node => CC+1
      else if = 2 edge, 1 node => CC +1
      & = +1 edge => CC +1
      or = +1 edge => CC +1

   * Did all methods (tools vs. manual count) get the same result?
      No.
   * Are the results clear?

2. Are the functions just complex, or also long?
   Some were complex, such as pairplot. But the others were long.
3. What is the purpose of the functions?
   essplots.py: Generate quantile, local, or evolution ESS plots
4. Are exceptions taken into account in the given measurements?
5. Is the documentation clear w.r.t. all the possible outcomes?
   essplots.py: yes.

## Refactoring

Plan for refactoring complex code:
essplot.py:


Estimated impact of refactoring (lower CC, but other drawbacks?).

Carried out refactoring (optional, P+):

git diff ...

## Coverage - essplot.py

### Tools

Document your experience in using a "new"/different coverage tool.

How well was the tool documented? Was it possible/easy/difficult to
integrate it with your build environment?

### Your own coverage tool

Show a patch (or link to a branch) that shows the instrumented code to
gather coverage measurements.

The patch is probably too long to be copied here, so please add
the git command that is used to obtain the patch instead:

git diff ...

What kinds of constructs does your tool support, and how accurate is
its output?

### Evaluation

1. How detailed is your coverage measurement?

2. What are the limitations of your own tool?

3. Are the results of your tool consistent with existing coverage tools?
It ran the following branches:
8
9
10
6
5
7
2
coverage: 89.1891891891892% 

missing are:
1, 3, 4 and 11.

Existing coverage tool: https://coverage.readthedocs.io/en/7.6.12/branch.html#how-to-measure-branch-coverage
gave: Name                     Stmts   Miss Branch BrPart  Cover
----------------------------------------------------------
arviz/plots/essplot.py      75      2     20      2    96%

Which differs from my test.

## Coverage improvement

Show the comments that describe the requirements for the coverage.

Report of old coverage: [link]

Report of new coverage: [link]



Test cases added:

git diff ...

Number of test cases added: two per team member (P) or at least four (P+).


## Self-assessment: Way of working

Current state according to the Essence standard: ...

Was the self-assessment unanimous? Any doubts about certain items?

How have you improved so far?

Where is potential for improvement?

## Overall experience

What are your main take-aways from this project? What did you learn?

Is there something special you want to mention here?
