# wembrey-palo-automation-journey
Repo for code samples supporting automation presentation


## Intro
This repo includes the sample files, and code snippets in a Jupyter notebook. To follow along, you need to start Jupyter from the bash shell and install pandevice.

The presentation runs through getting started with Palo Alto automation and learning how to automate or script certain jobs. It uses python and the pandevice module, the REST api, and uses python to parse a raw XML config file for offline work.


## Setup
This setup is written for Windows systems but for Unix bases systems, you can substitute "py -3" for "python3" and for the virtual environments, replace -venv/Scripts/activate" with "-venv/bin/activate".

1. On Windows, you'll want either the Ubuntu shell or just install Git. https://git-scm.com/downloads  

2. You'll also need python, so install 2 and 3. https://www.python.org/downloads/
Install both 2.7.X (latest) and 3 (latest) and be sure to **add python to path** for both of them. Once installed, you can run **Git Bash** and verify Python works.  
    > $ py -3 -V  
      _# Expected result_  
      Python 3.7.3  
  
  
3. Install Jupyter and ipython to use with Python3

    > $ pip3 install jupyter ipython  
      _# Expected_
      Collecting jupyter .....  
  
  
  
4. Clone this repository to your chosen location. Navigate to the parent directory and the following command will clone the repo and create the folder:

    > $ git clone https://github.com/ePlusPS/wembrey-palo-automation-journey.git  
  
  
  
5. Move into the directory and create your virtual environment

    > $ cd wembrey-palo-automation-journey  
      $ py -3 -m venv wpaj-venv  
  
  
  
6. Activate the virtual python environment, check it runs Python v3 and install pandevice

    > $ source wpaj-venv/Scripts/activate  
      (wpaj-venv)  
      $ py -V  
      Python 3.7.3  
      (wpaj-venv)  
      $ pip3 install pandevice  


  

  


  


