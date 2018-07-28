bucket="s3://recruitment-web-isfit-2019"
region="eu-west-1"
flags="--region $region --acl public-read --delete"

# deploy static files on in ./jobs/ to bucket
aws s3 sync . $bucket $flags --cache-control "public, no-cache, max-age=43200" \
  --exclude "*" \
  --include "jobs/*"

eb deploy recruitment-web-isfit-2019-prod
