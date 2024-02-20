import os
import sys

import aws_cdk as cdk
import pytest
from aws_cdk.assertions import Template


@pytest.fixture(scope="function")
def stack_defaults() -> None:
    os.environ["CDK_DEFAULT_ACCOUNT"] = "111111111111"
    os.environ["CDK_DEFAULT_REGION"] = "us-east-1"

    # Unload the app import so that subsequent tests don't reuse
    if "stack" in sys.modules:
        del sys.modules["stack"]


def test_synthesize_stack() -> None:
    import stack

    app = cdk.App()

    project_name = "test-project"
    dep_name = "test-deployment"
    mod_name = "test-module"
    app_prefix = f"{project_name}-{dep_name}-{mod_name}"

    vpc_id = "vpc-123"
    subnet_ids = []
    ecr_repo_name = "repo"
    task_cpu_units = 4 * 1024
    task_memory_limit_mb = 8 * 1024
    autoscale_max_capacity = 2
    artifacts_bucket_name = "bucket"

    stack = stack.MlflowFargateStack(
        scope=app,
        id=app_prefix,
        app_prefix=app_prefix,
        vpc_id=vpc_id,
        subnet_ids=subnet_ids,
        ecs_cluster_name=None,
        service_name=None,
        ecr_repo_name=ecr_repo_name,
        task_cpu_units=task_cpu_units,
        task_memory_limit_mb=task_memory_limit_mb,
        autoscale_max_capacity=autoscale_max_capacity,
        artifacts_bucket_name=artifacts_bucket_name,
        lb_access_logs_bucket_name=None,
        lb_access_logs_bucket_prefix=None,
        env=cdk.Environment(
            account=os.environ["CDK_DEFAULT_ACCOUNT"],
            region=os.environ["CDK_DEFAULT_REGION"],
        ),
    )

    template = Template.from_stack(stack)
    template.resource_count_is("AWS::ECS::Cluster", 1)
    template.resource_count_is("AWS::ECS::TaskDefinition", 1)