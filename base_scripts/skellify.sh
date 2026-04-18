for source in base base_scripts templates Makefile ruff.toml
do
    echo ${source}
    rsync \
        --exclude replace_skellington.py \
        --archive \
        --verbose \
        ../skellington/${source} .
done
