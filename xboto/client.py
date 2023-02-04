"""
You can import any client boto supports from this module and use it as if that's the current,
thread-safe client.

There are type-hints on the module for common clients we use,
but you can import anything boto supports.

If you import something boto does not support, you'll get an error only when you first
attempt to use the imported client.

```python
# Simply import and use it as-if it's a ready-to-go client.
# (you can use `xboto.client` for clients)
from xboto.client import ssm

# You can use it just like the normal boto3 ssm client.
# Every time you use it, it will lazily lookup the current one for the current thread.
ssm_paginator = ssm.get_paginator('get_parameters_by_path')
```

Lazily creating the clients helps support unit-testing with moto,
also reusing the same client lets boto reuse the same connection.

This module allows you to easily share them in a way that supports not directly
tying code together.

If you have an aws client that uses a `-` for it's name, you can use an `_` (underscore)
instead.
All underscores are changed to a `-` when looking up the aws client.
You can also directly use the `xboto.dependencies.BotoClients.load` method, and use a `-` there.

"""
from typing import Any

# These annotations are only for IDE-type-completion;
# any client boto supports will work when asked for.
# if you ask for an unsupported boto client, error will be raised when you first use it
# (not when you import it).
#
# Underscores are turned into `-` for us when client/resource is looked-up
accessanalyzer: Any
account: Any
acm: Any
acm_pca: Any
alexaforbusiness: Any
amp: Any
amplify: Any
amplifybackend: Any
amplifyuibuilder: Any
apigateway: Any
apigatewaymanagementapi: Any
apigatewayv2: Any
appconfig: Any
appconfigdata: Any
appflow: Any
appintegrations: Any
application_autoscaling: Any
application_insights: Any
applicationcostprofiler: Any
appmesh: Any
apprunner: Any
appstream: Any
appsync: Any
arc_zonal_shift: Any
athena: Any
auditmanager: Any
autoscaling: Any
autoscaling_plans: Any
backup: Any
backup_gateway: Any
backupstorage: Any
batch: Any
billingconductor: Any
braket: Any
budgets: Any
ce: Any
chime: Any
chime_sdk_identity: Any
chime_sdk_media_pipelines: Any
chime_sdk_meetings: Any
chime_sdk_messaging: Any
chime_sdk_voice: Any
cleanrooms: Any
cloud9: Any
cloudcontrol: Any
clouddirectory: Any
cloudformation: Any
cloudfront: Any
cloudhsm: Any
cloudhsmv2: Any
cloudsearch: Any
cloudsearchdomain: Any
cloudtrail: Any
cloudtrail_data: Any
cloudwatch: Any
codeartifact: Any
codebuild: Any
codecatalyst: Any
codecommit: Any
codedeploy: Any
codeguru_reviewer: Any
codeguruprofiler: Any
codepipeline: Any
codestar: Any
codestar_connections: Any
codestar_notifications: Any
cognito_identity: Any
cognito_idp: Any
cognito_sync: Any
comprehend: Any
comprehendmedical: Any
compute_optimizer: Any
config: Any
connect: Any
connect_contact_lens: Any
connectcampaigns: Any
connectcases: Any
connectparticipant: Any
controltower: Any
cur: Any
customer_profiles: Any
databrew: Any
dataexchange: Any
datapipeline: Any
datasync: Any
dax: Any
detective: Any
devicefarm: Any
devops_guru: Any
directconnect: Any
discovery: Any
dlm: Any
dms: Any
docdb: Any
docdb_elastic: Any
drs: Any
ds: Any
dynamodb: Any
dynamodbstreams: Any
ebs: Any
ec2: Any
ec2_instance_connect: Any
ecr: Any
ecr_public: Any
ecs: Any
efs: Any
eks: Any
elastic_inference: Any
elasticache: Any
elasticbeanstalk: Any
elastictranscoder: Any
elb: Any
elbv2: Any
emr: Any
emr_containers: Any
emr_serverless: Any
es: Any
events: Any
evidently: Any
finspace: Any
finspace_data: Any
firehose: Any
fis: Any
fms: Any
forecast: Any
forecastquery: Any
frauddetector: Any
fsx: Any
gamelift: Any
gamesparks: Any
glacier: Any
globalaccelerator: Any
glue: Any
grafana: Any
greengrass: Any
greengrassv2: Any
groundstation: Any
guardduty: Any
health: Any
healthlake: Any
honeycode: Any
iam: Any
identitystore: Any
imagebuilder: Any
importexport: Any
inspector: Any
inspector2: Any
iot: Any
iot_data: Any
iot_jobs_data: Any
iot_roborunner: Any
iot1click_devices: Any
iot1click_projects: Any
iotanalytics: Any
iotdeviceadvisor: Any
iotevents: Any
iotevents_data: Any
iotfleethub: Any
iotfleetwise: Any
iotsecuretunneling: Any
iotsitewise: Any
iotthingsgraph: Any
iottwinmaker: Any
iotwireless: Any
ivs: Any
ivschat: Any
kafka: Any
kafkaconnect: Any
kendra: Any
kendra_ranking: Any
keyspaces: Any
kinesis: Any
kinesis_video_archived_media: Any
kinesis_video_media: Any
kinesis_video_signaling: Any
kinesis_video_webrtc_storage: Any
kinesisanalytics: Any
kinesisanalyticsv2: Any
kinesisvideo: Any
kms: Any
lakeformation: Any
# Lambda is a key-word, underscore is ignored.
lambda_: Any
lex_models: Any
lex_runtime: Any
lexv2_models: Any
lexv2_runtime: Any
license_manager: Any
license_manager_linux_subscriptions: Any
license_manager_user_subscriptions: Any
lightsail: Any
location: Any
logs: Any
lookoutequipment: Any
lookoutmetrics: Any
lookoutvision: Any
m2: Any
machinelearning: Any
macie: Any
macie2: Any
managedblockchain: Any
marketplace_catalog: Any
marketplace_entitlement: Any
marketplacecommerceanalytics: Any
mediaconnect: Any
mediaconvert: Any
medialive: Any
mediapackage: Any
mediapackage_vod: Any
mediastore: Any
mediastore_data: Any
mediatailor: Any
memorydb: Any
meteringmarketplace: Any
mgh: Any
mgn: Any
migration_hub_refactor_spaces: Any
migrationhub_config: Any
migrationhuborchestrator: Any
migrationhubstrategy: Any
mobile: Any
mq: Any
mturk: Any
mwaa: Any
neptune: Any
network_firewall: Any
networkmanager: Any
nimble: Any
oam: Any
omics: Any
opensearch: Any
opensearchserverless: Any
opsworks: Any
opsworkscm: Any
organizations: Any
outposts: Any
panorama: Any
personalize: Any
personalize_events: Any
personalize_runtime: Any
pi: Any
pinpoint: Any
pinpoint_email: Any
pinpoint_sms_voice: Any
pinpoint_sms_voice_v2: Any
pipes: Any
polly: Any
pricing: Any
privatenetworks: Any
proton: Any
qldb: Any
qldb_session: Any
quicksight: Any
ram: Any
rbin: Any
rds: Any
rds_data: Any
redshift: Any
redshift_data: Any
redshift_serverless: Any
rekognition: Any
resiliencehub: Any
resource_explorer_2: Any
resource_groups: Any
resourcegroupstaggingapi: Any
robomaker: Any
rolesanywhere: Any
route53: Any
route53_recovery_cluster: Any
route53_recovery_control_config: Any
route53_recovery_readiness: Any
route53domains: Any
route53resolver: Any
rum: Any
s3: Any
s3control: Any
s3outposts: Any
sagemaker: Any
sagemaker_a2i_runtime: Any
sagemaker_edge: Any
sagemaker_featurestore_runtime: Any
sagemaker_geospatial: Any
sagemaker_metrics: Any
sagemaker_runtime: Any
savingsplans: Any
scheduler: Any
schemas: Any
sdb: Any
secretsmanager: Any
securityhub: Any
securitylake: Any
serverlessrepo: Any
service_quotas: Any
servicecatalog: Any
servicecatalog_appregistry: Any
servicediscovery: Any
ses: Any
sesv2: Any
shield: Any
signer: Any
simspaceweaver: Any
sms: Any
sms_voice: Any
snow_device_management: Any
snowball: Any
sns: Any
sqs: Any
ssm: Any
ssm_contacts: Any
ssm_incidents: Any
ssm_sap: Any
sso: Any
sso_admin: Any
sso_oidc: Any
stepfunctions: Any
storagegateway: Any
sts: Any
support: Any
support_app: Any
swf: Any
synthetics: Any
textract: Any
timestream_query: Any
timestream_write: Any
transcribe: Any
transfer: Any
translate: Any
voice_id: Any
waf: Any
waf_regional: Any
wafv2: Any
wellarchitected: Any
wisdom: Any
workdocs: Any
worklink: Any
workmail: Any
workmailmessageflow: Any
workspaces: Any
workspaces_web: Any
xray: Any


def __getattr__(name: str):
    if not name or name.startswith("_"):
        raise AttributeError(f"module {__name__} has no attribute {name}")

    # Reserve upper-case for future potential feature (ie: grab dependency class).
    if name[0].isupper():
        raise AttributeError(
            f"module {__name__} has no attribute {name} (use lower-case attr; ie: {name.lower()})."
        )

    from .dependencies import BotoClients
    return BotoClients.proxy_attribute(name)
