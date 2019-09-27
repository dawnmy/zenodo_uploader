# zenodo_uploader
batch upload to Zenodo

### Prerequirements

This script requires following Python packages to be installed: `requests`, `click`

### Usage

```
Usage: zenodo_uploader.py [OPTIONS] TOKEN METADATA [FILES]...

Options:
  -s, --sandbox  Test in sandbox for uploading
  --help         Show this message and exit.
```

The access token and json file of metadata (an example is in the `data` folder) must be provided. You can upload multiple files. Please ensure all files uplaoded are correct before publish because you can not delete the submission after publish, but you can still modify the metadata.
