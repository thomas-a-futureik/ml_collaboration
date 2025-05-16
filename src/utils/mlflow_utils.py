import mlflow
import os
import sys

##mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

def get_experiment_id(name):
    exp = mlflow.get_experiment_by_name(name)
    if exp is None:
      exp_id = mlflow.create_experiment(name)
      return exp_id
    return exp.experiment_id

def get_last_run_id(exp_name):
    exp = get_experiment_id(exp_name)
    client = mlflow.MlflowClient()
    runs = client.search_runs(experiment_ids=exp)
    if len(runs) == 0:
        return None
    last_run = runs[0]
    return last_run.info.run_id


