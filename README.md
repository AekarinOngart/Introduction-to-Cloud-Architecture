gcloud builds submit --tag gcr.io/modular-magpie-348711/fluckbook-fontend --project=modular-magpie-348711

gcloud  run deploy fluckbook-fontend --image gcr.io/modular-magpie-348711/fluckbook-fontend --platform managed --project=modular-magpie-348711 --allow-unauthenticated --region us-central1	

gcloud iam service-accounts list --project=modular-magpie-348711

gcloud iam service-accounts keys create ./key.json --iam-account github-action@modular-magpie-348711.iam.gserviceaccount.com

gcloud auth activate-service-account --key-file=key.json