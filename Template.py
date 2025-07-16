import os

structure = {
    "Multi_Container_LangChain":{
        "Orchestrator":{
            "app":{
                "__init__.py":None,
                "main.py":None,
                "orchestrator.py":None
            },
            "tests":{
                "__init__.py":None,
                "test_main.py":None
            },
            "DockerFile":None,
            "requirements.txt":None
        },
        "rag_chatbot":{
            "app":{
                "__init__.py":None,
                "main.py":None,
                "rag_utils.py":None
            },
            "tests":{
                "__init__.py":None,
                "test_main.py":None
            },
            "DockerFile":None,
            "requirements.txt":None
        },
        "text_to_sql":{
            "app":{
                "__init__.py":None,
                "main.py":None,
                "sql_generator.py":None
            },
            "tests":{
                "__init__.py":None,
                "test_main.py":None
            },
            "DockerFile":None,
            "requirements.txt":None
        }
    },
    "docker-compose.yml":None,
    ".env":None
}

def create_structure(base_path,struct):
    for name,content in struct.items():
        path = os.path.join(base_path,name)
        if content is None:
            with open(path,"w") as f:
                f.write("")
        else:
            os.makedirs(path,exist_ok=True)
            create_structure(path,content)

base_directory = "."
create_structure(base_directory,structure)
print("Directory Template created successfully.")