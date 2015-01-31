FileBucket
----------

- Usage -

Options:
  -h, --help            show this help message and exit
  -d  --seed			the seed file from which the target file is created (required)
  -s  --size			the size of the target file in megabytes (required)
  -f  --file			the target file path and name (can only be specified when NOT using the count option)
  -p  --prefix			the prefix to add to the random file name which can include a path (can only be used with the count option)
  -u  --suffix			the suffix to add to the random file name (can only be used with the count option)
  -c  --count			the number of files to write (optional)
  -k  --kilobyte		create files that are 1KB in size (cannot be used in conjunction with the --size or --seed options)

- Theory -

The program will create files of arbitrary size. Just provide it with a seed file provided
and it will generate a given file in a directory of your choice.