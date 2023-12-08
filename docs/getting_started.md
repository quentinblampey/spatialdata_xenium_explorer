## Installation

`spatialdata_xenium_explorer` can be installed on every OS with `pip` or [`poetry`](https://python-poetry.org/docs/) on `python>=3.10`.

!!! note "Advice (optional)"

    We advise creating a new environment via a package manager (except if you use Poetry, which will automatically create the environment).

    For instance, you can create a new `conda` environment:

    ```bash
    conda create --name spatialdata_xenium_explorer python=3.10
    conda activate spatialdata_xenium_explorer
    ```

Choose one of the following, depending on your needs (it should take at most a few minutes):

=== "From PyPI"

    ``` bash
    pip install spatialdata_xenium_explorer
    ```

=== "Local install (pip)"

    ``` bash
    git clone https://github.com/quentinblampey/spatialdata_xenium_explorer.git
    cd spatialdata_xenium_explorer

    pip install .
    ```

=== "Poetry (dev mode)"

    ``` bash
    git clone https://github.com/quentinblampey/spatialdata_xenium_explorer.git
    cd spatialdata_xenium_explorer

    poetry install --all-extras
    ```

## Usage

You can choose between these two options:

- Our [command-line-interface](../cli) (CLI)
- Our [python API](../api)