aws s3api create-bucket --bucket s3-test --endpoint-url=http://localhost:4566 \
--create-bucket-configuration LocationConstraint=ap-northeast-1

aws s3 cp ./株式会社auditcheck_test.xlsx s3://s3-test --profile localstack --endpoint-url http://localhost:4566
