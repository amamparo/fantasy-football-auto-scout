from aws_cdk.aws_ecs import ContainerImage
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService, ApplicationLoadBalancedTaskImageOptions
from aws_cdk.aws_iam import Role, PolicyDocument, PolicyStatement, Effect, ServicePrincipal
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.core import Stack, Construct, App, Duration
import os


class MainStack(Stack):
    def __init__(self, scope: Construct, _id: str, **kwargs) -> None:
        super().__init__(scope, _id, **kwargs)
        container_port = 5000
        yahoo_proxy_server = ApplicationLoadBalancedFargateService(
            self,
            'yahoo-proxy-server',
            memory_limit_mib=512,
            cpu=256,
            task_image_options=ApplicationLoadBalancedTaskImageOptions(
                image=ContainerImage.from_asset(
                    os.getcwd(),
                    file='Dockerfile',
                    exclude=['cdk.out'],
                    build_args={
                        'PROXY_PORT': str(container_port)
                    }
                ),
                container_port=container_port
            ),
            listener_port=80,
            public_load_balancer=True,
            desired_count=1,
            max_healthy_percent=100,
            min_healthy_percent=0
        )

        lambda_role = Role(
            self,
            'LambdaRole',
            assumed_by=ServicePrincipal('lambda.amazonaws.com'),
            inline_policies={
                's3': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            effect=Effect.ALLOW,
                            actions=[
                                's3:ListBucket',
                                's3:PutObject',
                                's3:GetObject',
                                's3:ListObjects'
                            ],
                            resources=[
                                'arn:aws:s3:::*'
                            ]
                        )
                    ]
                ),
                'lambda': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            effect=Effect.ALLOW,
                            actions=['lambda:InvokeFunction'],
                            resources=['arn:aws:lambda:*:*:function:*']
                        )
                    ]
                ),
                'logs': PolicyDocument(
                    statements=[
                        PolicyStatement(
                            effect=Effect.ALLOW,
                            actions=[
                                'logs:CreateLogGroup',
                                'logs:CreateLogStream',
                                'logs:PutLogEvents'
                            ],
                            resources=['*']
                        )
                    ]
                )
            }
        )

        Function(
            self,
            'scrape-league-settings-function',
            runtime=Runtime.PYTHON_3_7,
            code=Code.from_asset('.build', exclude=['boto3', 'flask']),
            handler='src.jobs.scrape_league_settings.main.lambda_handler',
            role=lambda_role,
            environment={
                'PROXY_BASE_URL': yahoo_proxy_server.load_balancer.load_balancer_dns_name,
                'LEAGUE_ID': os.environ.get('LEAGUE_ID'),
                'REQUEST_COOKIE': os.environ.get('REQUEST_COOKIE')
            },
            timeout=Duration.minutes(15),
            memory_size=1024
        )


if __name__ == '__main__':
    app = App()
    MainStack(app, 'fantasy-football-auto-scout')
    app.synth()
