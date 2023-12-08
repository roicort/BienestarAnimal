# PIBA - Plataforma Integral de Bienestar Animal


docker build --platform linux/amd64 --build-arg SA_KEY_BASE64=`base64 ./_gcp_sa/sa-artifact-registry.json` --progress=plain -t us-central1-docker.pkg.dev/mty-god-webservices-qa/mty-django/mty-empleo:0.1.0 .

docker run -it -p 8080:8080 --env-file ./env -v './_gcp_sa:/app/_gcp_sa' us-central1-docker.pkg.dev/mty-god-webservices-qa/mty-django/mty-empleo:0.1.0

docker push us-central1-docker.pkg.dev/mty-god-webservices-qa/mty-django/mty-empleo:0.1.0