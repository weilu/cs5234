def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator)

