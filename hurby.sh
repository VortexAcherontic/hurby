container_name="hurby"

hurby_cfg="$PWD/../hurby_cfg"

podman build . -t ${container_name}
podman rm ${container_name}

podman run --name ${container_name} \
	-v "$hurby_cfg:/root/.z-ray/hurby" \
	-e HURBY_DEVMODE=0 \
	-d ${container_name}
