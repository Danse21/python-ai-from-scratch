# Docker packages entire application (python version, dependencies, code, model files) into a
# container that runs identically on any machine.

# Base image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install uv
RUN pip install uv

# Copy and install dependencies
COPY Module_6_9_Docker/requirements.txt requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt

# pull all needed files into the container
COPY config.py .
COPY biodata.db .
COPY Module_6_8_FastAPI/ ./Module_6_8_FastAPI/

# Final working directly inside the container
WORKDIR /app/Module_6_8_FastAPI
EXPOSE 8000

# Command to run when container starts
CMD ["uvicorn", "async_endpoint:app", "--host", "0.0.0.0", "--port", "8000"]


# What does -p 8000:8000 mean in the docker run command?
# Answer: -p 8000:8000 means -p <host_port>:<container_port>. It maps a port on local machine (host) to a port inside the container.
# The -p makes it possible for external (localhost) network to reach the isolated container's network by default.
# Why do we COPY requirements.txt and RUN pip install before COPY . . (pulling all needed files into the container?
# What would happen if we did it the other way around?
# Answer: It is about Docker's layer caching. Each instruction (like COPY or RUN) creates a cached layer, and Docker only
# rebuilds a layer (and everything after it) if its inputs changed. So, copying requirements.txt and running pip install
# first means that layer only reruns when dependencies actually change. Doing it the other way around will cause invalidating
# the cache for that layer (COPY . .) if a single line of code in the needed files changes and force a full dependency
# reinstall on every rebuild. That will further slow down the process.
# What does --host 0.0.0.0 do, and why is it necessary inside a container?
# Answer: 0.0.0.0 means listen on all networks interfaces, ie., that accept connections from both localhost and container's
# internal network. The -p 8000:8000 mapping does this by forwarding traffic to the container's interanal network interface.
