# PDF コントラスト調整ツール

手書き文書をスキャンした PDF の字が薄くて読みづらい時用

WSL 上での使用を想定

## Requirements

- python 3.8.5
- poetry ^1.1.12
- poppler

## Usage

1. execute `poetry install`
2. Edit ./config.toml as ./config-examle.toml

- PDF files in "input_dir" are converted and outputed to "output_dir".
- After that, the origin PDF files in "input_dir" are removed.
- "alpha" and "beta" means contrast and brightness.
  $dst = \alpha*src + \beta$

3. execute `make`
