curl https://pyenv.run | bash

export PATH="/root/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv install 3.8.0

pyenv virtualenv 3.8.0 spiaggiari
pyenv activate spiaggiari
pip install -r requirements.txt