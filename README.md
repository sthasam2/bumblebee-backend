# Bumblebee

A social media for YOU

---

### Dependedencies

#### **Main Dependencies**

*   **Python 3.8**
*   **pip** ( python default package manager)
*   **poetry** ( Package and virtualenv manager | `pip install poetry`)
*   **PostgreSQL** (database | *[Check docs for full setup process](https://github.com/sthasam2/bumblebee-backend/blob/main/docs/database_setup.md)*)

## Installation

### **MANUAL SETUP**

1. **Setup a virtuial environment**

* *install virtualenv using* `pip install virtualenv`

* *create a virtualenv in the repo base directory using*  `virtualenv .venv`

2. **Activate virtualenv**
* **Windows** 

``` powershell
.venv\scripts\activate
```

* **Linux**

``` BASH
source .venv/bin/activate
```

3. **After all the mentioned dependencies are installed, run command:**

``` python
poetry install
```

This will install all the required dependencies for the project using the **poetry.lock** file which are needed for the projects.  
  
To check more dependencies enter command 

``` python
poetry show
```