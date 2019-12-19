from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'neos',
    'depends_on_past': False,
    'start_date': datetime(1970, 1, 1),
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'kube_sample', default_args=default_args, schedule_interval=None)


start = DummyOperator(task_id='t1', dag=dag)

passing = KubernetesPodOperator(namespace='airflow-dev',
                          image="python:3.6-slim",
                        #   cmds=["Python","-c"],
                        #   arguments=["print('hello world')"],
                          labels={"app": "airflow"},
                          node_selectors={"role": "data-pipeline"},
                          service_account_name="sa-airflow",
                          name="passing-test",
                          in_cluster=True,
                          task_id="passing-task",
                          get_logs=True,
                          volumes=[],
                          volume_mounts=[],
                          dag=dag
                          )

failing = KubernetesPodOperator(namespace='airflow-dev',
                          image="ubuntu",
                        #   cmds=["Python","-c"],
                        #   arguments=["print('hello world')"],
                          labels={"app": "airflow"},
                          node_selectors={"role": "data-pipeline"},
                          service_account_name="sa-airflow",
                          name="fail",
                          in_cluster=True,
                          task_id="failing-task",
                          get_logs=True,
                          dag=dag
                          )

passing.set_upstream(start)
failing.set_upstream(start)