# The repo show vibration data of elevator.

## Develop Environment Setup
* Install MySQL  
  In my.cnf set:  
    ```[mysqld]  
    lower_case_table_names=1  
    character_set_server=utf8  
  ```
* Install (python2.7)  
  Install python libs with following commands  
  ```bash
  sudo apt-get install python-mysql
  sudo apt-get instal python-pyside
  sudo pip install dataset
  sudo pip install numpy
  sudo pip install matplotlib
  sudo pip install seaborn 
  sudo pip install scipy
  ```