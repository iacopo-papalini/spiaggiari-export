export PATH="/root/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate spiaggiari

echo "$(date) Start"
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}" || exit
python "${DIR}/bin/fetch_documents.py" "$@" 2>&1
echo "$(date) End"