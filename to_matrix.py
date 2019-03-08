import src.DictToMatrix as DictToMatrix

if __name__ == '__main__':
    data_dir = "./data/pickled_files/"
    out_data_dir = "./data/matrix_files/"

    data = DictToMatrix.DictToMatrix()
    data.run(data_dir, out_data_dir)
