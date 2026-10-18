# La base est fournie par config/openfoam.env, avec son digest d'index.
ARG BLCFD_OPENFOAM_IMAGE
FROM ${BLCFD_OPENFOAM_IMAGE}

USER root
# L'image OpenCFD seule ne contient pas Python. Git permet de tracer le commit.
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 git \
    && rm -rf /var/lib/apt/lists/*
