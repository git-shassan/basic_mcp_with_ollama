# podman build -t mcp:latest ./
# podman run -it --net host --rm mcp:latest /bin/bash
FROM registry.access.redhat.com/ubi9/ubi
LABEL description="Syed MCP Server" 
MAINTAINER Syed Hassan 
    # Install dependencies
RUN dnf install \
        wget \
	nodejs \
	python3.12 python3-pip -y
RUN pip install -qU duckduckgo-search langchain-community ddgs
RUN wget https://go.dev/dl/go1.25.3.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.25.3.linux-amd64.tar.gz
RUN rm go1.25.3.linux-amd64.tar.gz && mkdir /root/mcpconfig/
ENV PATH=$PATH:/usr/local/go/bin
COPY ./.mcphost.yml /root/mcpconfig/.mcphost.yml 
# alternatively, mount the directory
RUN /usr/local/go/bin/go install github.com/mark3labs/mcphost@latest
CMD /root/go/bin/mcphost --config /root/mcpconfig/.mcphost.yml
