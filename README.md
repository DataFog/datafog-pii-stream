# datafog-piistream-demo

## PII Observability
A simple demo UI application and corresponding backend that shows real-time PII detection in a streaming environment.

Built with ❤️ using Datafog x Redpanda x Spark x Streamlit 


## Demo Setup
```sh
% git clone https://github.com/DataFog/datafog-piistream-demo.git
% cd datafog-piistream-demo
% docker compose up
# Open a browser to http://localhost:8501 to use the UI
% docker exec -it redpanda-1 rpk topic consume pii-detection # view detected output
```