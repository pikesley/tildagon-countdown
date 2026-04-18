TAG=$(uuidgen)
APP=$(basename $(pwd))
OUTDIR=/tmp/${APP}

. ${HOME}/.config/emf/tildagon


echo "building"

rm -fr ${OUTDIR}
mkdir -p ${OUTDIR}

git tag ${TAG}

git archive --format tar --prefix ${APP}/ ${TAG} > ${OUTDIR}/rc.tar

if [ "${1}" == "deploy" ]
then
    echo "deploying"
    cd ${OUTDIR}

    tar xvf rc.tar

    cd ${APP}
    python -m mpremote fs rm -r :/apps/${APP}
    python -m mpremote fs mkdir :/apps/${APP}
    python -m mpremote fs cp -r * :/apps/${APP}
fi

if [ "${1}" == "simulate" ]
then
    cd ${TILDAGON_SIMULATOR}/apps
    rm -fr ${APP}
    tar xvf ${OUTDIR}/rc.tar
    cd ../
    pipenv run python run.py
fi
