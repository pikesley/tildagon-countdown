. ${HOME}/.config/emf/tildagon
ln -s $(pwd) ${TILDAGON_SIMULATOR}/apps
cd ${TILDAGON_SIMULATOR} && \
pipenv run python run.py
