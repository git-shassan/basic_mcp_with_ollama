# podman build -t mcp:latest ./
# podman run -it --net host --rm mcp:latest /bin/bash
# A default MCP config is copied, But alternatively, mount the directory with this file locally using : "-v ./:/root/mcpconfig/:z"
FROM registry.access.redhat.com/ubi9/ubi
LABEL description="Syed MCP Server" 
MAINTAINER Syed Hassan 
    # Install dependencies
RUN dnf install \
        wget \
	nodejs \
	python3.12 python3-pip -y
# if adding podman client is desired: 
# that will require to run: "podman system service tcp:IP:PORT --time=0" on server. e.g: 192.168.22.4:8888
# ...and when launching container, pass environment variable REMOTE_PODMAN with this value
RUN dnf install podman -y ; alias docker=podman;
# 
RUN pip install -qU duckduckgo-search langchain-community ddgs
RUN wget https://go.dev/dl/go1.25.3.linux-amd64.tar.gz
RUN tar -C /usr/local -xzf go1.25.3.linux-amd64.tar.gz
RUN rm go1.25.3.linux-amd64.tar.gz && mkdir /root/mcpconfig/
ENV PATH=$PATH:/usr/local/go/bin
COPY ./.mcphost.yml /root/mcpconfig/.mcphost.yml 
RUN /usr/local/go/bin/go install github.com/mark3labs/mcphost@latest
# if using podman client
CMD ["/usr/bin/bash", "-c","podman system connection add myserver tcp://$REMOTE_PODMAN; /root/go/bin/mcphost --config /root/mcpconfig/.mcphost.yml"]
# if not using podman client
#CMD ["/usr/bin/bash", "-c","/root/go/bin/mcphost --config /root/mcpconfig/.mcphost.yml"]
