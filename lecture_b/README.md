# Lecture B: Tensors in NumPy and PyTorch

## NumPy and PyTorch tensors
To find more information about the topics discussed during the lecture, have a look at
- [NumPy quickstart](https://numpy.org/doc/1.26/user/quickstart.html)
- [NumPy indexing](https://numpy.org/doc/1.26/user/basics.indexing.html)
- [NumPy broadcasting](https://numpy.org/doc/1.26/user/basics.broadcasting.html)
- [NumPy documentation](https://numpy.org/doc/1.26/)
- [Python profilers](https://docs.python.org/3/library/profile.html)
- [PyTorch tensor class reference](https://pytorch.org/docs/1.13/tensors.html)

If the behavior of your local instance differs from the documentation, check that you are looking at the right version of the documentation. There is usually a drop-down menu at the top of the page. Pip shows the versions of all installed packages with
```bash
pip3 freeze
```

## Setting up VertexAI training environment on Google Cloud

### Setting up Google Cloud Vertex AI
1. Create a Google Account if you do not have one
2. Login to Google Cloud [here](https://cloud.google.com/) and redeem your credits
3. Create a new project
4. Activate the VertexAI API by searching for "vertexai"
5. Go to "Training" in the sidebar on the left and select the region "europe-west4". Your runs will appear here
6. Increase the GPU-quota: Type "all quotas" into the search bar and search for "aiplatform.googleapis.com/custom_model_training_nvidia_t4_gpus" next to the filter and then add "europe-west4" to the filter. Check the checkbox next to the quota, click "Edit quota" and request an increase to 1. **It will take up to two business days to be processed and then up to five business days to be increased, so account for that time!** You will receive email updates to your GMail address about the quota request. You can proceed however without the quota increase, but you will not be able to launch jobs which require GPUs.

### Setting up the Vertex AI Python SDK

#### Create a storage bucket for your code
1. Search for "cloud storage"
2. Click "Create", give the bucket a name
3. Select region type "Region" and choose the region `europe-west4`
4. The final settings can remain defaut, confirm the bucket

#### Set up a service account and download credentials
1. Search for "service accounts" in AIM & Admin
2. Create a new service account and give it any name
3. Add the roles "Vertex AI Custom Code Service Agent", "Service Account User" and "Storage Object Admin"
4. The final settings can remain defaut, confirm the service account
5. Open the service account and switch to the "Keys" tab
6. Create a new key in the JSON format. A `.json` file should be downloaded.
7. Name the `.json` file `credentials.json` and place it in the `msindnns` root directory

#### Change local settings
In the `launch_vertex_job.py` script, set
- `PROJECT` to the project ID of your project, to be found e.g. in the [console](https://console.cloud.google.com/)
- `BUCKET` to the URI of the bucket you created, it is "gs://" followed by the bucket id found e.g. in the bucket details
- `N_GPUS` specifies the numbers of GPUs to use. You can set it to 0 for testing purposes if your quota increase has not yet been approved.

Furthermore, create an empty file `wandb_key.json` in the root directory. We will later use this.

### Launching jobs
Jobs can be submitted to the Google Cloud hardware either as a Python script or as a package. In both cases, the submission is done via the [`launch_vertex_job.py`](/launch_vertex_job.py) script. To get an overview of the options, run
```bash
python3 launch_vertex_job.py script --help
python3 launch_vertex_job.py package --help
```

The experiment the run ends up in can be set with the `EXPERIMENT` constant in the launch script.

Note: For the output of your code to end up in the log file as described below, you need to include these lines at the top of your script / the module you run:
```python
if "LOG_PATH" in os.environ:
    os.makedirs(os.path.dirname(os.environ["LOG_PATH"]), exist_ok=True)
    log = open(os.environ["LOG_PATH"], "a")
    sys.stdout = log
	sys.stderr = log
```

#### Launching a script
If your code is just a single Python file, you can use the `script` option to submit it. You need to specify the name of the job, the path to the script file as well as arguments you want to pass to the script. 

The script is run inside a special environment called a Docker container which includes PyTorch 1.13 and dependencies like NumPy pre-installed and all requirements from the course virtual environment are always included as well. If you need additional requirements, you can add them

To submit the script `hello_world_vertex_ai/hello_world_script.py` with command line arguments `--text1 "hello from" --text2 google`, run
```bash
python3 launch_vertex_job.py script --name hello_world_script --path ./lecture_b/hello_world_vertex_ai/hello_world_script.py --requirements asciimatics --args --text1 "hello from" --text2 google
```
You will see some output in the terminal about the state of the job and links to the job's page on Google Cloud. It is normal to take a few minutes for the job to be pending before it starts. The output of your script will be saved in a text file in the storage bucket in a subdirectory with the name of the job and a timestamp from when you ran the launch script. If you do not want to receive continuous updates about the job's state in the terminal, you can just press Ctrl+c. The job will continue running.

#### Launching a package
If your code is spread out over several Python files, it needs to be a Python package. The submissions script then bundles the code into a source distribution (a compressed file) which is uploaded to your stogare bucket, before the job is launched.

To make your code into a Python package, move all modules and sub-packages (directories with `__init__.py` files) into a new directory with (an empty) `__init__.py` file. Then create a file `setup.py` in the root directory. You should now have this directory structure
```
root
├── package_name
│   ├── sub_package_1
│   │   ├── __init__.py
│   │   └── sub_module_1.py
│   ├── __init__.py
│   ├── module_1.py
│   └── module_2.py
└── setup.py
```
Have a look for the files in `hello_world_vertex_ai` for an example.

The `setup.py` should have the following content
```python
from setuptools import find_packages
from setuptools import setup

setup(
    name="hello-world",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    description="Hello World",
)
```
You can change the description of the package and should include all packages which are required on top of `torch`, `numpy` etc. in `install_requires`, as a list of strings in pip syntax, e.g. `["lightning==2.1.2", "torchvision==0.14.0"]`. The code is run in the same Docker container as the scripts. You should adjust the name of the package to something descriptive for the task you are working on.

To use your package locally, install it in editable mode into the virtual environment by running
```bash
pip3 install -e .
```
in the root directory. To avoid clashes with your work on other tasks, set a unique name in the `setup.py`. Now you can run the hello world package locally with `python3 main.py` as usual.

To launch your package, use the `package` option to `launch_vertex_job.py` and supply the name of the job, the path to the root directory of the package, the module to be run from within your package in Python import syntax (e.g. `package_name.module_1` in the example above) and the command line arguments to be passed to the module. To launch the module `main` in the `hello_world` package with argument `--text1 "hello from" --text2 google`, run e.g.
```bash
python3 launch_vertex_job.py package --name hello_world_package --directory ./lecture_b/hello_world_vertex_ai --task-module hello_world.main --args --text1 "hello from" --text2 google
```

The output of your script is written to a text file in the same directory in your storage bucket, to which the launcher uploads the source distribution. You can find it under "Package locations" in the job's detail page.
